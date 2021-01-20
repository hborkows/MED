from basic.basic import basic_ar
from cumulate.cumulate import cumulate_ar
from utils.taxonomy import Taxonomy
from configparser import ConfigParser
from utils.io import read_taxonomy, read_transactions, read_item_list
from typing import Callable, List
import sys
import pickle
import time
import random


def get_association_rules(_algorithm: Callable, _dataset: List, _taxonomy: Taxonomy,
                          min_sup: float = 25, min_conf: float = 60.0):
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
            random.seed(17)
            transactions = random.sample(transactions, 40000)
        #transactions = read_transactions(transactions_path, taxonomy=taxonomy)
        #with open(transactions_path, 'wb') as file:
        #    pickle.dump(transactions, file)
        with open(items_path, 'rb') as file:
            item_list = pickle.load(file)
    elif data_mode == 'txt':
        item_list = read_item_list(items_path)
        with open(items_path, 'wb') as file:
            pickle.dump(item_list, file)
        taxonomy = read_taxonomy(taxonomy_path, items=item_list)
        with open(taxonomy_path, 'wb') as file:
            pickle.dump(taxonomy, file)
        transactions = read_transactions(transactions_path, taxonomy=taxonomy)
        with open(transactions_path, 'wb') as file:
            pickle.dump(transactions, file)
    else:
        sys.exit(1)

    if measure_time:
        for algorithm in algorithms:
            start = time.time()
            print(f'Doing {algorithm.__name__}')
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
