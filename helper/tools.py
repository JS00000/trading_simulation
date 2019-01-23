# coding=utf-8
import datetime
import calendar
import dateutil.parser
import numpy as np
from scipy import stats

def convert_string_to_timestamp(st):
    return calendar.timegm(dateutil.parser.parse(st).timetuple())

def convert_timestamp_to_datetime(ti):
    return datetime.datetime.utcfromtimestamp(ti)

def calc_mssk(x):
    mu = np.mean(x, axis=0)
    sigma = np.std(x, axis=0)
    skew = stats.skew(x)
    kurtosis = stats.kurtosis(x)
    print(mu, sigma, skew, kurtosis)