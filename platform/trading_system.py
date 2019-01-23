# coding=utf-8

import pandas as pd
import numpy as np
import types

from base.mongodb.document import Stock, CryptoDay, CryptoHour, CryptoMinute

class TradeMarket(object):

    def __init__(self, code, his_data, columns):
        self.code = code
        self.his_data = his_data
        self.order = []
        self.columns = columns
        self.p_ma = his_data.max()[1]
        self.p_mi = his_data.min()[2]
        self.v_ma = his_data.max()[4]
        self.v_mi = his_data.min()[4]
        self.last_close = his_data.iloc[-1]['close']
        self.last_volumn = his_data.iloc[-1]['volume']

    def get_last_data(self):
        return self.his_data.iloc[-1]

    def get_seq_data(self, seq_length):
        return self.his_data[-seq_length:]

    def get_scare_para(self):
        return (self.p_ma, self.p_mi, self.v_ma, self.v_mi)

    # ty == 0: sell
    # ty == 1: buy
    def add_order(self, price, ty, volume, user_id):
        self.order.append([price, ty, volume, user_id])

    def auction(self):
        self.order.sort(key=lambda s: (s[0], s[1]))
        sell_sum = np.zeros(len(self.order))
        sell_min = 1e9
        buy_sum = np.zeros(len(self.order))
        buy_max = 0
        ss = 0
        for i in range(len(self.order)):
            if self.order[i][1] == 0:
                ss += self.order[i][2]
                if sell_min == 1e9:
                    sell_min = self.order[i][0]
            sell_sum[i] = ss
        ss = 0
        for i in range(len(self.order)-1, -1, -1):
            if self.order[i][1] == 1:
                ss += self.order[i][2]
                if buy_max == 0:
                    buy_max = self.order[i][0]
            buy_sum[i] = ss
        last_close = self.last_close
        final_open = last_close
        final_close = sell_min
        final_volumn = -1
        final_amount = -1
        if sell_min > buy_max:
            final_high = final_low = final_close = final_open
            final_p_change = final_volumn = final_amount = 0
        else:
            final_high = buy_max
            final_low = sell_min
            for i in range(len(self.order)):
                v = min(buy_sum[i], sell_sum[i])
                if v > final_volumn:
                    final_volumn = v
                    final_close = self.order[i][0]
                if v == final_volumn:
                    if abs(final_close - last_close) > abs(self.order[i][0] - last_close):
                        final_close = self.order[i][0]
            if final_open == 0:
                final_p_change = 0
            else:
                final_p_change = (final_close - final_open) / final_open
            final_amount = final_volumn * final_close
        if self.p_ma < final_high:
            self.p_ma = final_high
        if self.p_mi > final_low:
            self.p_mi = final_low
        if self.v_ma < final_volumn:
            self.v_ma = final_volumn
        if self.v_mi > final_volumn:
            self.v_mi = final_volumn
        next_data = [final_open, final_high, final_low, final_close, final_volumn, final_amount, final_p_change]
        index_value = self.his_data.index.values
        next_time = index_value[-1] - index_value[-2] + index_value[-1]
        df = pd.DataFrame([next_data], index=[next_time], columns=self.columns)
        self.his_data = self.his_data.append(df)
        self.last_close = final_close
        self.last_volumn = final_volumn

    def get_result(self):
        # [user_id, code, price, ty, volume]
        ret = []
        p = self.last_close
        v = self.last_volumn
        for i in range(len(self.order)):
            if self.order[i][1] == 0 and self.order[i][0] <= p:
                if v > self.order[i][2]:
                    v -= self.order[i][2]
                    ret.append( ( self.order[i][3], self.code, p, 0, self.order[i][2] ) )
                else:
                    ret.append( ( self.order[i][3], self.code, p, 0, v ) )
                    break
        v = self.last_volumn
        for i in range(len(self.order)-1, -1, -1):
            if self.order[i][1] == 1 and self.order[i][0] >= p:
                if v > self.order[i][2]:
                    v -= self.order[i][2]
                    ret.append( ( self.order[i][3], self.code, p, 1, self.order[i][2] ) )
                else:
                    ret.append( ( self.order[i][3], self.code, p, 1, v ) )
                    break
        self.order = []
        return ret

class Tradengine(object):

    def __init__(self, codes, start_date="2017-9-01", end_date="2018-01-01", **options):

        # Initialize codes.
        self.codes = codes

        # Initialize data frames.
        self.origin_frames = dict()

        # Initialize parameters.
        self._init_options(**options)

        # Initialize data.
        self._init_data(start_date, end_date)

        # Initialize Market.
        self._init_market()

    def _init_options(self, **options):

        try:
            self.m_type = options['market']
        except KeyError:
            self.m_type = 'stock'

        try:
            self.logger = options['logger']
        except KeyError:
            self.logger = None

        try:
            self.seq_length = options['seq_length']
        except KeyError:
            self.seq_length = 5
        finally:
            self.seq_length = self.seq_length if self.seq_length > 1 else 2

        if self.m_type == 'stock':
            self.doc_class = Stock
        elif self.m_type == 'crypto_day':
            self.doc_class = CryptoDay
        elif self.m_type == 'crypto_hour':
            self.doc_class = CryptoHour
        elif self.m_type == 'crypto_minute':
            self.doc_class = CryptoMinute

    def _init_data(self, start_date, end_date):
        self._init_data_frames(start_date, end_date)

    def _validate_codes(self):
        if not self.code_count:
            raise ValueError("Codes cannot be empty.")
        for code in self.codes:
            if not self.doc_class.exist_in_db(code):
                raise ValueError("Code: {} not exists in database.".format(code))

    def _init_data_frames(self, start_date, end_date):
        # Remove invalid codes first.
        self._validate_codes()
        # Init columns and data set.
        self.columns = ['open', 'high', 'low', 'close', 'volume', 'amount', 'p_change']
        dates_set = set()
        # Load data.
        for code in self.codes:
            # Load instrument docs by code.
            instrument_docs = self.doc_class.get_k_data(code, start_date, end_date)
            # Init instrument dicts.
            instrument_dicts = [instrument.to_dic() for instrument in instrument_docs]
            # Split dates.
            dates = [instrument[1] for instrument in instrument_dicts]
            # Split instruments.
            instruments = [instrument[2:] for instrument in instrument_dicts]
            # Update dates set.
            dates_set = dates_set.union(dates)
            # Build origin frames.
            origin_frame = pd.DataFrame(data=instruments, index=dates, columns=self.columns)
            # Build code - frame map.
            self.origin_frames[code] = origin_frame
        # Init date iter.
        self.dates = sorted(list(dates_set))
        # Rebuild index.
        for code in self.codes:
            origin_frame = self.origin_frames[code]
            self.origin_frames[code] = origin_frame.reindex(self.dates, method='bfill')

    def _origin_data(self, code, date):
        date_index = self.dates.index(date)
        return self.origin_frames[code].iloc[date_index]

    def _init_market(self):
        self.market = dict()
        for code in self.codes:
            self.market[code] = TradeMarket(code, self.origin_frames[code], self.columns)

    def get_ori_data(self):
        return [self.origin_frames[code].iloc[-self.seq_length:] for code in self.codes]

    def get_new_data(self):
        data = []
        for code in self.codes:
            instruments = self.market[code].get_seq_data(self.seq_length)
            data.append(np.array(instruments))
        data = np.array(data)
        ret = []
        for seq_index in range(self.seq_length):
            ret.append(data[:, seq_index, :].reshape((-1)))
        ret = np.array(ret)
        return ret

    def get_scare_para(self):
        return [self.market[code].get_scare_para() for code in self.codes]

    def print_new_data(self):
        print(self.codes)
        for code in self.codes:
            print(code)
            print(self.market[code].get_seq_data(self.seq_length))


    def add_order(self, code, price, ty, volume, user_id):
        self.market[code].add_order(price, ty, volume, user_id)

    def auction(self):
        for code in self.codes:
            self.market[code].auction()

    def get_result(self):
        ret = []
        for code in self.codes:
            ret.extend(self.market[code].get_result())
        return ret

    def get_last_data(self):
        ret = []
        for code in self.codes:
            ret.append(self.market[code].get_last_data())
        return ret

    @property
    def code_count(self):
        return len(self.codes)

    @property
    def data_dim(self):
        return self.code_count * self.origin_frames[self.codes[0]].shape[1]
