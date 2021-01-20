from utils.taxonomy import Taxonomy
from typing import List
from itertools import combinations
from utils.alg_utils import get_frequent_1_set, generate_hash_tree, generate_k_subsets, is_prefix, prune
import time


def frequent_itemsets_apriori(transactions: List, min_sup: float):
    frequent_itemsets = get_frequent_1_set(transactions, min_sup)
    #print(frequent_itemsets)
    prev_frequent = [itemset[0] for itemset in frequent_itemsets]
    #print(prev_frequent)
    length = 2
    while len(prev_frequent) > 1:
        candidates = []
        for i in range(len(prev_frequent)):
            j = i + 1
            while j < len(prev_frequent) and is_prefix(prev_frequent[i], prev_frequent[j]):
                #print('check')
                #print(prev_frequent[i][:-1])
                #print([prev_frequent[i][-1]] )
                #print([prev_frequent[j][-1]])
                candidates.append(list(prev_frequent[i][:-1]) + [prev_frequent[i][-1]] + [prev_frequent[j][-1]])
                j += 1

        tree = generate_hash_tree(candidate_itemsets=candidates, length=length)
        k_subsets = generate_k_subsets(transactions=transactions, prev_frequent=prev_frequent, length=length)
        #print('Pruning')
        #k_subsets = prune(k_subsets, prev_frequent, length)
        print(f'candidates: {candidates}')
        del candidates
        del prev_frequent

        print(f'{length}_subsets len: {len(k_subsets)}')

        # Calculate support for k_subsets and add to hash_tree
        for subset in k_subsets:
            tree.add_support(subset)

        del k_subsets

        new_frequent = tree.get_frequent_itemsets(min_sup=min_sup)
        print(f'new_frequent 1: {new_frequent}')
        del tree
        '''tmp_new_frequent = []
        for item in new_frequent:
            for subitem in item:
                if subitem:
                    tmp_new_frequent.append(subitem)
        new_frequent = tmp_new_frequent'''
        #print(f'candidates: {candidates}')
        if new_frequent:
            frequent_itemsets.extend(new_frequent)
            prev_frequent = [tup[0] for tup in new_frequent]
            #prev_frequent =
            prev_frequent.sort()
        else:
            prev_frequent = []
        length += 1
        del new_frequent
        #del tmp_new_frequent
        print(f'prev_frequent: {prev_frequent}')

    return frequent_itemsets


def basic_ar(transactions: List, taxonomy: Taxonomy, min_sup: float, min_conf: float):
    # Add ancestors from taxonomy to transactions
    transactions_w_ancestors = []
    for transaction in transactions:
        for item in transaction:
            ancestors = taxonomy.get_ancestors(item)
            if ancestors:
                ancestors = [item for item in ancestors if item]
                transaction.extend(ancestors)
        new_transaction = list(set([item.node_id for item in transaction]))
        transactions_w_ancestors.append(new_transaction)

    freq_itemsets = frequent_itemsets_apriori(transactions_w_ancestors, min_sup)
    #print(f'f_itemsets: {freq_itemsets}')
    hash_map = {}
    #lefts = []
    for itemset in freq_itemsets:
        hash_map[tuple(itemset[0])] = itemset[1]
        #lefts.append(itemset[0])

    result = []
    for itemset in freq_itemsets:
        if len(itemset[0]) == 1:
            continue

        union_support = hash_map[tuple(itemset[0])]
        for i in range(1, len(itemset[0])):
            #print(f'h_map: {hash_map}')
            lefts = map(list, combinations(itemset[0], i))
            for left in lefts:
                #print(f'left: {tuple(left)}')
                try:
                    conf = 100 * union_support / hash_map[tuple(left)]
                    if conf >= min_conf:
                        result.append([left, list(set(itemset[0]) - set(left)), conf])
                except KeyError:
                    pass


    return result
