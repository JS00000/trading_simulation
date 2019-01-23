# coding=utf-8

import tushare as ts
import logging

from base.mongodb.document import Stock
from helper.args_parser import stock_spider_parser


class StockSpider(object):
    def __init__(self, code, start="2008-01-01", end="2018-01-01"):
        self.code = code
        self.start = start
        self.end = end

    def crawl(self):
        stock_frame = ts.get_k_data(code=self.code, start=self.start, end=self.end, retry_count=30)
        last = stock_frame.loc[0]['close']
        for index in stock_frame.index:
            stock_series = stock_frame.loc[index]
            stock_dict = stock_series.to_dict()
            stock = Stock(**stock_dict)
            stock.p_change = (stock_series['close'] - last) / last
            last = stock_series['close']
            stock.save_if_need()
        logging.warning("Finish crawling code: {}, items count: {}".format(self.code, stock_frame.shape[0]))

def main(args):
    codes = args.codes
    # codes = ['sh']
    for _code in codes:
        StockSpider(_code, args.start, args.end).crawl()


if __name__ == '__main__':
    main(stock_spider_parser.parse_args())
