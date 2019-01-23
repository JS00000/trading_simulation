# coding=utf-8

import logging
import requests

from base.mongodb.document import CryptoDay
from helper.args_parser import crypto_day_spider_parser
from helper.tools import convert_string_to_timestamp, convert_timestamp_to_datetime

class CryptoDaySpider(object):

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
            # 86400 * 2000 = 172800000
            if (self.end - self.start >= 172800000):
                toTs = self.start + 172800000 - 1
                limit = 2000
                self.start = self.start + 172800000
            else:
                toTs = self.end
                limit = (self.end - self.start) // 86400 + 1
                self.start = self.end + 1

            # get limit+1 data
            payload = {"fsym":self.code, "tsym":self.tsym, "limit":limit, "toTs":toTs}
            r = requests.get("https://min-api.cryptocompare.com/data/histoday", params = payload)
            r.raise_for_status()
            print(r.url)
            if (r.json()['Response'] == 'Success'):
                data = r.json()['Data']
                last = data[0]['close']
                for it in data[1:]:
                    cd = CryptoDay()
                    cd.code = self.code
                    cd.date = convert_timestamp_to_datetime(it['time'])
                    cd.low = it['low']
                    cd.high = it['high']
                    cd.open = it['open']
                    cd.close = it['close']
                    cd.volume = it['volumefrom']
                    cd.amount = it['volumeto']
                    cd.p_change = (it['close'] - last) / last
                    last = it['close']
                    cd.save_if_need()
                logging.warning("Finish crawling code: {}, items count: {}".format(self.code, len(data)))

def main(args):
    for code in args.codes:
        for tsym in args.tsyms:
            CryptoDaySpider(code, tsym, args.start, args.end).crawl()


if __name__ == '__main__':
    main(crypto_day_spider_parser.parse_args())