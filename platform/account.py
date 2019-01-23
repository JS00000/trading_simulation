import math

from enum import Enum

class ActionCode(Enum):
    Sell = 0
    Buy = 1
    Hold = 2

class Matter(object):

    def __init__(self, code="None", buy_price=0, volume=0):
        self.code = code
        self.volume = volume
        self.buy_price = buy_price
        self.cur_price = buy_price
        self.cur_value = self.cur_price * self.volume

    def add(self, buy_price, volume):
        self.buy_price = (self.volume * self.buy_price + volume * buy_price) / (self.volume + volume)
        self.volume += volume
        self.update_status(buy_price)

    def sub(self, sell_price, volume):
        self.volume -= volume
        self.update_status(sell_price)

    def hold(self, cur_price):
        self.update_status(cur_price)

    def update_status(self, cur_price):
        self.cur_price = cur_price
        self.cur_value = self.cur_price * self.volume

class Account(object):

    def __init__(self, codes, fund, init_data):
        # Init cash, market, codes.
        self.codes = codes
        self.cash = fund / (self.codes_count + 1)
        # Init holding matters.
        self.matters = dict()
        for code_id, code in enumerate(codes):
            price = init_data[code_id].iloc[-1]['close']
            volume = fund / (self.codes_count + 1) / price
            self.matters[code] = Matter(code, price, volume)
        # Init initial cash.
        self.initial_fund = fund
        # Init history profits.
        self.history_profits = []
        # Init action dic.
        self.action_dic = {ActionCode.Sell: self.sell, ActionCode.Buy: self.buy, ActionCode.Hold: self.hold}

    @property
    def codes_count(self):
        return len(self.codes)

    @property
    def action_space(self):
        return self.codes_count * 3

    @property
    def assets(self):
        return self.cash + self.holdings_value

    @property
    def profits(self):
        return self.cash + self.holdings_value - self.initial_fund

    @property
    def holdings_value(self):
        holdings_value = 0
        # Accumulate matter value.
        for code in self.codes:
            holdings_value += self.matters[code].cur_value
        return holdings_value

    def get_volume(self):
        return [self.matters[code].volume for code in self.codes]

    def buy(self, code, price, volume):
        # Check if volume is valid.
        volume = volume if self.cash > price * volume else int(math.floor(self.cash / price))
        # If volume > 0, means cash is enough.
        if volume > 0:
            self.matters[code].add(price, volume)
            # Update cash and holding price.
            self.cash -= volume * price
        else:
            self.matters[code].update_status(price)

    def sell(self, code, price, volume):
        # Sell matter if possible.
        volume = volume if volume < self.matters[code].volume else self.matters[code].volume
        self.matters[code].sub(price, volume)
        # Update cash and holding price.
        self.cash += volume * price

    def hold(self, code, price, volume):
        self.matters[code].update_status(price)

    def action_by_code(self, code):
        return self.action_dic[ActionCode(code)]

    def update_profits(self):
        self.history_profits.append(self.profits)