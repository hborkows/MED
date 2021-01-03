from utils.taxonomy import Taxonomy
from utils.hash_tree import HashTree
from typing import List
from itertools import combinations


def frequent_itemsets(transactions: List, min_sup: float):
    return []


def basic_ar(transactions: List, taxonomy: Taxonomy, min_interest: float, min_sup: float, min_conf: float):
    freq_itemsets = frequent_itemsets(transactions, min_sup)
    hash_map = {}
    for itemset in freq_itemsets:
        hash_map[tuple(itemset[0])] = itemset[1]

    result = []
    for itemset in freq_itemsets:
        if len(itemset[0]) == 1:
            continue

        union_support = hash_map[tuple(itemset[0])]
        for i in range(1,len(itemset[0])):
            lefts = map(list, combinations(itemset[0], i))
            for left in lefts:
                conf = 100.0 * union_support / hash_map[tuple(left)]
                if conf >= min_conf:
                    result.append([left, list(set(itemset[0]) - set(left)), conf])

    return result
