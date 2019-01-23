# coding=utf-8

import numpy as np

from account import Account
from predictor.normal.rand import Rand

class User(Account):

    def __init__(self, user_id, codes, fund, init_data, stratigy_id):
        super(User, self).__init__(codes, fund, init_data)
        self.user_id = user_id

        if stratigy_id == 0:
            # Random predictor
            self.predictor = Rand(stratigy_id)
        else:
            # other predictor
            pass
        self.predict = self.predictor.predict

        # rate of receive global information
        # can be a distribution among tot fund
        self.receive_rate = 0.01

        # rate of transfer information
        # can be a distribution among 
        self.transfer_rate = 0.5

        self.info = dict()

        # every step the value in info decay by 0.8, than after 10 steps, the value is less than 0.1 * origin_value
        self.info_decay = 0.8

    def update_info(self, info_id, info_value):
        if info_id not in self.info:
            # self.info[info_id] = info_value
            self.info[info_id] = np.random.normal(info_value, 1)

    def get_info(self):
        return self.info

    def get_receive_rate(self):
        return self.receive_rate

    def get_transfer_rate(self):
        return self.transfer_rate
    
    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def decide(self, input_data, scare_para):
        # input_data is the last history OHLCV data
        # scare_para is max/min price/volume in all history data

        # ta is the prediction of the price using history data, range in [-1, 1]. 
        # ta = -1 means one's prediction is down, 1 is up, 0 is don't know
        # ta is the quantification of Technical Analysis
        ta = self.predict(input_data, scare_para)

        # fa is the prediction of the price using information, range in [-1, 1]
        # fa = -1 means one's prediction is down, 1 is up, 0 is don't know
        # fa is the quantification of Fundamental Analysis
        info_sum = 0.
        for k in self.info:
            info_sum += self.info[k]
        fa = self._sigmoid(info_sum) * 2 - 1

        # average of ta and fa
        analysis = (ta + fa) / 2

        decision = dict()

        # decide whether sell(0) or buy(1) or hold(2)
        hold_rate = 0.5 - abs(2 * analysis)
        if hold_rate < 0:
            hold_rate = 0
        buy_rate = 0.5 * analysis + 0.5
        partition = [(1 - buy_rate) * (1 - hold_rate), buy_rate * (1 - hold_rate), hold_rate]
        # print("par", partition)
        decision['action_id'] = np.random.choice(3,size=1,p=partition)[0]

        # decide which price to sell or buy
        # ±20%
        last_price = input_data[-1][3]
        decision['price'] = (last_price * (1 + analysis / 5))

        # decide how much to sell or buy
        # here we just use the first bond
        percent = np.power(np.random.random(), 0.1 / abs(analysis))
        decision['percent'] = percent
        if decision['action_id'] == 0: #sell
            decision['volume'] = (self.get_volume()[0] * percent)
            # decision['price'] *= 0.95
        elif decision['action_id'] == 1: #buy
            decision['volume'] = (self.cash / decision['price'] * percent)
            # decision['price'] *= 1.05
        else:
            decision['volume'] = 0
        decision['code'] = self.codes[0]

        return decision

    def status_update(self, price):
        for idx, code in enumerate(self.codes):
            self.action_by_code(2)(code, price[idx]['close'], 0)
        self.update_profits()
        for k in self.info.copy():
            self.info[k] = self.info[k] * self.info_decay
            if abs(self.info[k]) < 0.1:
                del self.info[k]