# coding=utf-8

import logging
import requests

from base.mongodb.document import CryptoMinute
from helper.args_parser import crypto_minute_spider_parser
from helper.tools import convert_string_to_timestamp, convert_timestamp_to_datetime

class CryptoMinuteSpider(object):

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
            # 60 * 2000 = 120000
            if (self.end - self.start >= 120000):
                toTs = self.start + 120000 - 1
                limit = 2000
                self.start = self.start + 120000
            else:
                toTs = self.end
                limit = (self.end - self.start) // 60 + 1
                self.start = self.end + 1

            # get limit+1 data
            payload = {"fsym":self.code, "tsym":self.tsym, "limit":limit, "toTs":toTs}
            r = requests.get("https://min-api.cryptocompare.com/data/histominute", params = payload)
            r.raise_for_status()
            print(r.url)
            if (r.json()['Response'] == 'Success'):
                data = r.json()['Data']
                last = data[0]['close']
                for it in data[1:]:
                    cm = CryptoMinute()
                    cm.code = self.code
                    cm.date = convert_timestamp_to_datetime(it['time'])
                    cm.low = it['low']
                    cm.high = it['high']
                    cm.open = it['open']
                    cm.close = it['close']
                    cm.volume = it['volumefrom']
                    cm.amount = it['volumeto']
                    cm.p_change = (it['close'] - last) / last
                    last = it['close']
                    cm.save_if_need()
                logging.warning("Finish crawling code: {}, items count: {}".format(self.code, len(data)))


def main(args):
    for code in args.codes:
        for tsym in args.tsyms:
            CryptoMinuteSpider(code, tsym, args.start, args.end).crawl()


if __name__ == '__main__':
    main(crypto_minute_spider_parser.parse_args())