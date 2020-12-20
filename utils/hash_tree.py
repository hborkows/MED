class Node:
    def __init__(self):
        self.children = {}
        self.is_leaf = True
        self.bucket = {}


class HashTree:
    def __init__(self, itemset_size: int, leaf_capacity: int):
        self._root = Node()
        self._itemset_size = itemset_size
        self._leaf_capacity = leaf_capacity

    def _insert_r(self, node: Node, itemset: tuple, index: int, count: int):
        # last bucket
        if index == len(itemset):
            if itemset in node.bucket:
                node.bucket[itemset] += count
            else:
                node.bucket[itemset] = count
            return

        # leaf node -> insert into bucket or transform into non-leaf for more space
        if node.is_leaf:
            if itemset in node.bucket:
                node.bucket[itemset] += count
            else:
                node.bucket[itemset] += count

            # no space left in leaf -> transform into non-leaf node
            if len(node.bucket) >= self._leaf_capacity:
                for old_itemset, old_count in node.bucket.items():
                    hash_key = self.hash_value(old_itemset[index])
                    if hash_key not in node.children.keys():
                        node.children[hash_key] = Node()
                    self._insert_r(node.children[hash_key], old_itemset, index + 1, old_count)

                del node.bucket
                node.is_leaf = False
        # non-leaf node -> continue to appropriate leaf node using hash_key
        else:
            hash_key = self.hash_value(itemset[index])
            if hash_key not in node.children.keys():
                node.children[hash_key] = Node()
            self._insert_r(node.children[hash_key], itemset, index + 1, count)

    def insert(self, itemset):
        itemset = tuple(itemset)
        self._insert_r(self._root, itemset, 0, 0)

    def hash_value(self, value):
        return value % self._leaf_capacity

    def add_support(self, itemset):
        current_node = self._root
        index = 0
        while True:
            if current_node.is_leaf:
                if itemset in current_node.bucket:
                    current_node.bucket[itemset] += 1
                break
            hash_key = self.hash_value(itemset[index])
            if hash_key in current_node.children.keys():
                current_node = current_node.children[hash_key]
            else:
                break
            index += 1

    def _dfs(self, node: Node, min_sup: int):
        if node.is_leaf:
            for key, value in node.bucket.items():
                if value >= min_sup:
                    return key, value
        else:
            result = []
            for child in node.children.keys():
                result.append(self._dfs(child, min_sup))
            return result

    def get_frequent_itemsets(self, min_sup: int):
        return self._dfs(self._root, min_sup)

