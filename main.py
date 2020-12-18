from basic.basic import basic_ar
from utils.taxonomy import Taxonomy
from utils.io import read_taxonomy, read_transactions, read_item_list
from typing import Callable, List


def get_association_rules(_algorithm: Callable, _dataset: List, _taxonomy: Taxonomy,
                          min_interest: float = 2, min_sup: float = 3, min_conf: float = 0.6):
    return _algorithm(_dataset, _taxonomy, min_interest, min_sup, min_conf)


if __name__ == '__main__':
    algorithms = [basic_ar]
    item_list = read_item_list('data/fruithut_original.txt')
    taxonomy = read_taxonomy('data/fruithut_taxonomy.txt')
    transactions = read_transactions('data/fruithut_original.txt', taxonomy=taxonomy)

    for algorithm in algorithms:
        result = get_association_rules(_algorithm=algorithm, _dataset=transactions, _taxonomy=taxonomy)
