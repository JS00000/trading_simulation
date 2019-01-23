# coding=utf-8

import numpy as np
import os

class Rand(object):
    def __init__(self, seed):
        # better 0 <= seed < 5
        self.p = seed*2+1

    def predict(self, x, scare_para):
        r = np.random.random()
        return np.power(2*r-1, self.p)
