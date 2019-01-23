# coding=utf-8

import networkx as nx

class Relationship(object):

    def __init__(self, n, seed):
        if seed == 0:
            # 空网络
            self.net = nx.empty_graph()
        elif seed == 1:
            # ER随机图
            self.net = nx.gnp_random_graph(n, 0.012)
        elif seed == 2:
            # ER随机图
            self.net = nx.gnp_random_graph(n, 0.1)
        elif seed == 3:
            # ER随机图
            self.net = nx.gnp_random_graph(n, 0.3)
        elif seed == 4:
            # 规则图
            self.net = nx.watts_strogatz_graph(n, 4, 0)
        elif seed == 5:
            # 规则图
            self.net = nx.watts_strogatz_graph(n, 8, 0)
        elif seed == 6:
            # 规则图
            self.net = nx.watts_strogatz_graph(n, 16, 0)
        elif seed == 7:
            # WS小世界网络
            self.net = nx.connected_watts_strogatz_graph(n, 4, 0.1)
        elif seed == 8:
            # WS小世界网络
            self.net = nx.connected_watts_strogatz_graph(n, 8, 0.1)
        elif seed == 9:
            # WS小世界网络
            self.net = nx.connected_watts_strogatz_graph(n, 16, 0.1)
        elif seed == 10:
            # 无标度网络
            self.net = nx.barabasi_albert_graph(n, 4)
        elif seed == 11:
            # 无标度网络
            self.net = nx.barabasi_albert_graph(n, 8)
        elif seed == 12:
            # 无标度网络
            self.net = nx.barabasi_albert_graph(n, 16)
        elif seed == 13:
            # 高斯随机分块网络
            self.net = nx.gaussian_random_partition_graph(n, 100, 10, 1, 0.01)
        elif seed == 14:
            # 高斯随机分块网络
            self.net = nx.gaussian_random_partition_graph(n, 100, 10, 1, 0.01)
        elif seed == 15:
            # 高斯随机分块网络
            self.net = nx.gaussian_random_partition_graph(n, 100, 10, 1, 0.01)
        else:
            self.net = nx.empty_graph()

        # print("seed=", seed)
        # print(nx.density(self.net))
        # print(nx.average_shortest_path_length(self.net))
        # print(nx.average_clustering(self.net))