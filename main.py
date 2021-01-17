from basic.basic import basic_ar
from cumulate.cumulate import cumulate_ar
from utils.taxonomy import Taxonomy
from configparser import ConfigParser
from utils.io import read_taxonomy, read_transactions, read_item_list
from typing import Callable, List
import sys
import pickle
import time


def get_association_rules(_algorithm: Callable, _dataset: List, _taxonomy: Taxonomy,
                          min_sup: float = 3, min_conf: float = 0.6):
    return _algorithm(_dataset, _taxonomy,min_sup, min_conf)


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config/main.conf')

    algorithms = [basic_ar, cumulate_ar]

    if config['Main']['data_mode'] == 'pickle':
        with open(config['Data']['taxonomy'], 'rb') as file:
            taxonomy = pickle.load(file)
        with open(config['Data']['transactions'], 'rb') as file:
            transactions = pickle.load(file)
        with open(config['Data']['items'], 'rb') as file:
            item_list = pickle.load(file)
    elif config['Main']['data_mode'] == 'txt':
        item_list = read_item_list(config['Data']['items'])
        taxonomy = read_taxonomy(config['Data']['taxonomy'], items=item_list)
        transactions = read_transactions(config['Data']['transactions'], taxonomy=taxonomy)
    else:
        sys.exit(1)

    if config['Main']['measure_time'] == 'yes':
        for algorithm in algorithms:
            start = time.time()
            result = get_association_rules(_algorithm=algorithm, _dataset=transactions, _taxonomy=taxonomy)
            end = time.time()
            delta = end - start
            print(f'Algorithm: {algorithm.__name__}:')
            print(f'Elapsed time: {delta}')
            print(result)
    elif config['Main']['measure_time'] == 'no':
        for algorithm in algorithms:
            result = get_association_rules(_algorithm=algorithm, _dataset=transactions, _taxonomy=taxonomy)
            print(f'Algorithm: {algorithm.__name__}:')
            print(result)
    else:
        sys.exit(1)
