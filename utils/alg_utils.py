from typing import List, Tuple
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
            result.append((tuple([key]), count))
    return result


def generate_k_subsets(transactions: List, prev_frequent: List, length: int):
    result = []
    for itemset in transactions:
        combs = map(list, combinations(itemset, length))
        result.extend(combs)
    '''i = 0
    for itemset in transactions:
        for freq in prev_frequent:
            freq = list(freq)
            if set(freq).issubset(set(itemset)):
                print(f'Adding combs {i}')
                i += 1
                combs = map(list, combinations(itemset, length))
                result.extend(combs)
                continue'''

    return result


def prune(candidateSet, prevFreqSet, length):
    tempCandidateSet = candidateSet.copy()
    for item in candidateSet:
        subsets = combinations(item, length)
        for subset in subsets:
            # if the subset is not in previous K-frequent get, then remove the set
            if frozenset(subset) not in prevFreqSet:
                tempCandidateSet.remove(item)
                print(f'removing: {item}')
                del item
                break
    return tempCandidateSet


def generate_hash_tree(candidate_itemsets, length, max_leaf_count=20, max_child_count=20):
    tree = HashTree(itemset_size=max_leaf_count, leaf_capacity=max_child_count)
    for itemset in candidate_itemsets:
        tree.insert(itemset)
    return tree


def is_prefix(list_1: List, list_2: List):
    for i in range(len(list_1) - 1):
        if list_1[i] != list_2[i]:
            return False
    return True
