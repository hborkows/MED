from basic.basic import basic_ar
from utils.taxonomy import Taxonomy, load_taxonomy, save_taxonomy
from utils.item import Item
from utils.utils import *
from typing import Callable, Set


def get_association_rules(_algorithm: Callable, _dataset: Set, _taxonomy: Taxonomy,
                          min_interest: float = 2, min_sup: float = 3, min_conf: float = 0.6):
    return _algorithm(dataset, taxonomy, min_interest, min_sup, min_conf)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    algorithms = [basic_ar]
    dataset = load_pickle('data/dataset.pkl')
    taxonomy = load_pickle('/data/taxonomy.pkl')

    for algorithm in algorithms:
        result = get_association_rules(_algorithm=algorithm, _dataset=dataset, _taxonomy=taxonomy)
