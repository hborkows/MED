from utils.taxonomy import Taxonomy
from utils.hash_tree import HashTree
from typing import List
from itertools import combinations


def get_frequent_1_set(transactions: List, min_sup: float):
    candidate_1_set = {}
    for transaction in transactions:
        for item in transaction:
            if item.node_id in candidate_1_set:
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


def frequent_itemsets_apriori(transactions: List, min_sup: float):
    frequent_itemsets = get_frequent_1_set(transactions, min_sup)
    prev_freqent = [itemset[0] for itemset in frequent_itemsets]
    length = 2
    while len(prev_freqent) > 1:
        candidates = []
        for i in range(len(prev_freqent)):
            j = i + 1
            while j < len(prev_freqent) and is_prefix(prev_freqent[i], prev_freqent[j]):
                candidates.append(prev_freqent[i][:-1] + [prev_freqent[i][-1]] + [prev_freqent[j][-1]])
                j += 1

        tree = generate_hash_tree(candidate_itemsets=candidates, length=length)
        k_subsets = generate_k_subsets(transactions=transactions, length=length)

        # Calculate support for k_subsets and add to hash_tree
        for subset in k_subsets:
            tree.add_support(subset)

        new_frequent = tree.get_frequent_itemsets(min_sup=min_sup)
        frequent_itemsets.extend(new_frequent)
        prev_freqent = [tup[0] for tup in new_frequent]
        prev_freqent.sort()
        length += 1

    return frequent_itemsets


def basic_ar(transactions: List, taxonomy: Taxonomy, min_interest: float, min_sup: float, min_conf: float):
    # Add ancestors from taxonomy to transactions
    transactions_w_ancestors = []
    for transaction in transactions:
        for item in transaction:
            transaction.extend(taxonomy.get_ancestors(item))
        new_transaction = list(set([item.node_id for item in transaction]))
        transactions_w_ancestors.append(new_transaction)

    freq_itemsets = frequent_itemsets_apriori(transactions_w_ancestors, min_sup)
    hash_map = {}
    for itemset in freq_itemsets:
        hash_map[tuple(itemset[0])] = itemset[1]

    result = []
    for itemset in freq_itemsets:
        if len(itemset[0]) == 1:
            continue

        union_support = hash_map[tuple(itemset[0])]
        for i in range(1, len(itemset[0])):
            lefts = map(list, combinations(itemset[0], i))
            for left in lefts:
                conf = 100.0 * union_support / hash_map[tuple(left)]
                if conf >= min_conf:
                    result.append([left, list(set(itemset[0]) - set(left)), conf])

    return result
