# coding=utf-8

import numpy as np
from scipy import stats
from user import User
from trading_system import Tradengine
from relationship import Relationship
from helper.tools import calc_mssk
from helper.args_parser import play_parser
from helper.data_ploter import plot_rank, plot_distribution, plot_imitate_market

def main(args):
    codes = args.codes
    start = args.start
    end = args.end
    market = args.market
    steps = args.steps
    user_number = args.user_number
    init_fund = args.init_fund
    transfer_deep = args.transfer_deep

    T = Tradengine(codes, start, end, **{
        "market": market,
        "seq_length": 5
    })

    U = []
    for i in range(user_number):
        # same stratigy
        U.append(User(i, codes, init_fund, T.get_ori_data(), 0))

    R = Relationship(user_number, 10)
    degree = R.net.degree()

    his_close = []
    his_p_change = []
    assets = np.ndarray(user_number)
    ass_deg = np.ndarray(user_number, dtype=[('assets', float), ('degree', int)])

    for step in range(steps):
        order_num = 0

        # generate random news
        info_value = np.random.normal(0, 1)

        # pass the news to user
        for i in range(user_number):
            if np.random.random() < U[i].get_receive_rate():
                U[i].update_info(step, info_value)

        # transfer the news along network for transfer_deep times
        for __ in range(transfer_deep):
            for i, to in R.net.adj.items():
                info_h = U[i].get_info()
                for to, _eattr in to.items():
                    if np.random.random() < U[i].get_transfer_rate():
                        for k in info_h:
                            U[to].update_info(k, info_h[k])

        # decide and add order
        for i in range(user_number):
            d = U[i].decide(T.get_new_data(), T.get_scare_para())
            if not (d['action_id'] == 2 or d['volume'] == 0):
                T.add_order(d['code'], d['price'], d['action_id'], d['volume'], i)
                order_num += 1

        # call auction
        T.auction()

        # conclude transactions
        r = T.get_result()
        for it in r:
            U[it[0]].action_by_code(it[3])(it[1], it[2], it[4])
        last_data = T.get_last_data()

        # update everyones assets
        for i in range(user_number):
            U[i].status_update(last_data)

        # results
        for i in range(user_number):
            assets[i] = U[i].assets
            ass_deg[i] = (U[i].assets, degree[i])

        his_close.append(last_data[0]['close'])
        his_p_change.append(last_data[0]['p_change'])
        # if (step+1) % 25 == 0:
        #     plot_distribution(assets)
        #     plot_imitate_market(his_close)
        print("step: ", step, last_data[0]['close'], last_data[0]['p_change'])

    plot_rank(ass_deg)
    plot_distribution(assets)
    plot_imitate_market(his_close)


if __name__ == '__main__':
    main(play_parser.parse_args())
