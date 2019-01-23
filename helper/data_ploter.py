# coding=utf-8

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import math

def plot_rank(x):
    x.sort(order='assets')
    l = len(x)
    data = np.ndarray(l)
    colors = np.ndarray((l,4))
    ma = 1
    mi = l
    for i in range(len(x)):
        data[i] = x[i][0]
        if ma < x[i][1]:
            ma = x[i][1]
        if mi > x[i][1]:
            mi = x[i][1]
    for i in range(len(x)):
        colors[i] = ((x[i][1] - mi) / (ma - mi), 0, 0, 1)
        
    plt.bar(range(l), data, color=colors)
    plt.title(u'Users: %d' % l)
    plt.show()

def plot_distribution(x):
    y1, x1, dummy = plt.hist(x, 100, normed=True)
    plt.title(u'Users: %d' % x.shape[0])
    plt.show()

def plot_imitate_market(y):
    plt.figure(figsize=(20, 15))
    plt.title("imitate_market")
    plt.plot(y, label="close price")
    plt.xlabel('Steps')
    plt.show()


def plot_cdf(x):
    pass