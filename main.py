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
    return _algorithm(_dataset, _taxonomy, min_sup, min_conf)


if __name__ == '__main__':
    config = ConfigParser()
    config.read('conf/main.conf')
    data_mode = config['Main']['data_mode']
    measure_time = True if config['Main']['measure_time'] == 'yes' else False
    transactions_path = config['Data']['transactions']
    taxonomy_path = config['Data']['taxonomy']
    items_path = config['Data']['items']

    algorithms = [basic_ar, cumulate_ar]

    if data_mode == 'pickle':
        with open(taxonomy_path, 'rb') as file:
            taxonomy = pickle.load(file)
        with open(transactions_path, 'rb') as file:
            transactions = pickle.load(file)
        with open(items_path, 'rb') as file:
            item_list = pickle.load(file)
    elif data_mode == 'txt':
        item_list = read_item_list(items_path)
        taxonomy = read_taxonomy(taxonomy_path, items=item_list)
        transactions = read_transactions(transactions_path, taxonomy=taxonomy)
    else:
        sys.exit(1)

    if measure_time:
        for algorithm in algorithms:
            start = time.time()
            result = get_association_rules(_algorithm=algorithm, _dataset=transactions, _taxonomy=taxonomy)
            end = time.time()
            delta = end - start
            print(f'Algorithm: {algorithm.__name__}:')
            print(f'Elapsed time: {delta}')
            print(result)
    else:
        for algorithm in algorithms:
            result = get_association_rules(_algorithm=algorithm, _dataset=transactions, _taxonomy=taxonomy)
            print(f'Algorithm: {algorithm.__name__}:')
            print(result)
