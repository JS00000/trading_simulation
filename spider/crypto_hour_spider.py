# coding=utf-8

import logging
import requests

from base.mongodb.document import CryptoHour
from helper.args_parser import crypto_hour_spider_parser
from helper.tools import convert_string_to_timestamp, convert_timestamp_to_datetime

class CryptoHourSpider(object):

    def __init__(self, code, tsym, start, end):
        self.code = code
        self.tsym = tsym
        self.start = convert_string_to_timestamp(start)
        self.end = convert_string_to_timestamp(end)

    def crawl(self):
        while (self.end >= self.start):
            toTs = 0
            limit = 0 
            # limit <= 2000 is required
            # 3600 * 2000 = 7200000
            if (self.end - self.start >= 7200000):
                toTs = self.start + 7200000 - 1
                limit = 2000
                self.start = self.start + 7200000
            else:
                toTs = self.end
                limit = (self.end - self.start) // 3600 + 1
                self.start = self.end + 1

            # get limit+1 data
            payload = {"fsym":self.code, "tsym":self.tsym, "limit":limit, "toTs":toTs}
            r = requests.get("https://min-api.cryptocompare.com/data/histohour", params = payload)
            r.raise_for_status()
            print(r.url)
            if (r.json()['Response'] == 'Success'):
                data = r.json()['Data']
                last = data[0]['close']
                for it in data[1:]:
                    ch = CryptoHour()
                    ch.code = self.code
                    ch.date = convert_timestamp_to_datetime(it['time'])
                    ch.low = it['low']
                    ch.high = it['high']
                    ch.open = it['open']
                    ch.close = it['close']
                    ch.volume = it['volumefrom']
                    ch.amount = it['volumeto']
                    ch.p_change = (it['close'] - last) / last
                    last = it['close']
                    ch.save_if_need()
                logging.warning("Finish crawling code: {}, items count: {}".format(self.code, len(data)))

def main(args):
    for code in args.codes:
        for tsym in args.tsyms:
            CryptoHourSpider(code, tsym, args.start, args.end).crawl()


if __name__ == '__main__':
    main(crypto_hour_spider_parser.parse_args())