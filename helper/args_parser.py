# coding=utf-8

import argparse

stock_codes = ["600036", "601328", "601998", "601398"]
stock_start = "2008-01-01"
stock_end   = "2019-01-01"
crypto_fsyms = ["BTC", "ETH", "LTC", "XRP", "EOS", "IOST", "DTA", "ZIL"]
crypto_tsyms = ["USD", "USDT"]
crypto_day_start = "2011-01-01"
crypto_day_end   = "2019-01-01"
crypto_hour_start = "2011-01-01"
crypto_hour_end   = "2019-01-01"
crypto_minute_start = "2019-01-17"
crypto_minute_end   = "2019-01-22"

stock_spider_parser = argparse.ArgumentParser()
stock_spider_parser.add_argument("-c", "--codes", default=stock_codes, nargs="+")
stock_spider_parser.add_argument("-s", "--start", default=stock_start)
stock_spider_parser.add_argument("-e", "--end", default=stock_end)

crypto_day_spider_parser = argparse.ArgumentParser()
crypto_day_spider_parser.add_argument("-c", "--codes", default=crypto_fsyms[:1], nargs="+")
crypto_day_spider_parser.add_argument("-t", "--tsyms", default=crypto_tsyms[:1], nargs="+")
crypto_day_spider_parser.add_argument("-s", "--start", default=crypto_day_start)
crypto_day_spider_parser.add_argument("-e", "--end", default=crypto_day_end)

crypto_hour_spider_parser = argparse.ArgumentParser()
crypto_hour_spider_parser.add_argument("-c", "--codes", default=crypto_fsyms[:1], nargs="+")
crypto_hour_spider_parser.add_argument("-t", "--tsyms", default=crypto_tsyms[:1], nargs="+")
crypto_hour_spider_parser.add_argument("-s", "--start", default=crypto_hour_start)
crypto_hour_spider_parser.add_argument("-e", "--end", default=crypto_hour_end)

crypto_minute_spider_parser = argparse.ArgumentParser()
crypto_minute_spider_parser.add_argument("-c", "--codes", default=crypto_fsyms[:1], nargs="+")
crypto_minute_spider_parser.add_argument("-t", "--tsyms", default=crypto_tsyms[:1], nargs="+")
crypto_minute_spider_parser.add_argument("-s", "--start", default=crypto_minute_start)
crypto_minute_spider_parser.add_argument("-e", "--end", default=crypto_minute_end)

play_parser = argparse.ArgumentParser()
play_parser.add_argument("-c", "--codes", default=crypto_fsyms[:1], nargs="+")
play_parser.add_argument("-s", "--start", default="2017-01-01")
play_parser.add_argument("-e", "--end", default="2019-01-01")
play_parser.add_argument("--market", default="crypto_day")
play_parser.add_argument("--steps", default=100, type=int)
play_parser.add_argument("--user_number", default=100, type=int)
play_parser.add_argument("--init_fund", default=100000, type=int)
play_parser.add_argument("--transfer_deep", default=1, type=int)
