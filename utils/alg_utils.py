from typing import List
from itertools import combinations
from utils.hash_tree import HashTree


def get_frequent_1_set(transactions: List, min_sup: float):
    candidate_1_set = {}
    for transaction in transactions:
        for item in transaction:
            if item in candidate_1_set:
                candidate_1_set[item] += 1
            else:
                candidate_1_set[item] = 1

    result = []
    for key, count in candidate_1_set.items():
        if count >= (min_sup * len(transactions) / 100):
            result.append(([key], count))
    return result


def generate_k_subsets(transactions: List, length: int):
    result = []
    for itemset in transactions:
        result.extend(map(list, combinations(itemset, length)))
    return result


def generate_hash_tree(candidate_itemsets, length, max_leaf_count=4, max_child_count=5):
    tree = HashTree(itemset_size=max_leaf_count, leaf_capacity=max_child_count)
    for itemset in candidate_itemsets:
        tree.insert(itemset)
    return tree


def is_prefix(list_1: List, list_2: List):
    for i in range(len(list_1) - 1):
        if list_1[i] != list_2[i]:
            return False
    return True
