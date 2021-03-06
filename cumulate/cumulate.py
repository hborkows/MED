from utils.alg_utils import get_frequent_1_set, generate_hash_tree, generate_k_subsets, is_prefix
from utils.taxonomy import Taxonomy
from typing import List
from itertools import combinations

item_ancestors = {}


def frequent_itemsets_apriori_cumulate(transactions: List, min_sup: float):
    global item_ancestors
    # TODO add optimisations from article
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

        # Optimization 3 -> remove pairs of [item ancestor]
        if length == 2:
            tmp_candidates = []
            for candidate in candidates:
                item_1 = candidate[0]
                item_2 = candidate[1]
                if item_1 not in item_ancestors[item_2] and item_2 not in item_ancestors[item_1]:
                    tmp_candidates.append(candidate)
            candidates = tmp_candidates

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


def cumulate_ar(transactions: List, taxonomy: Taxonomy, min_sup: float, min_conf: float):
    global item_ancestors
    transactions_w_ancestors = []
    for transaction in transactions:
        for item in transaction:
            ancestors = taxonomy.get_ancestors(item)
            if ancestors:
                ancestors = [item for item in ancestors if item]
                item_ancestors[item.node_id] = ancestors  # Optimization #2 -> pre-computing ancestors
                transaction.extend(ancestors)
        new_transaction = list(set([item.node_id for item in transaction]))
        transactions_w_ancestors.append(new_transaction)

    # TODO add optimisations from article
    freq_itemsets = frequent_itemsets_apriori_cumulate(transactions_w_ancestors, min_sup)
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
