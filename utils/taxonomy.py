from utils.item import Item
import pickle


def find_node_r(node: Item, name: str):
    if node.name == name:
        return node
    elif node.get_children():
        for child in node.get_children():
            result = find_node_r(child, name)
            if result:
                return result
        return None
    else:
        return None


class Taxonomy:
    def __init__(self):
        self._root = Item(name='__root__')

    def find_node(self, name: str):
        return find_node_r(self._root, name)

    def add_node(self, node: Item, parent_name: str):
        parent = self.find_node(parent_name)
        parent.add_child(node)


def save_taxonomy(taxonomy: Taxonomy, path: str):
    with open(path, 'wb') as file:
        pickle.dump(taxonomy, file)


def load_taxonomy(path: str):
    with open(path, 'rb') as file:
        return pickle.load(file)
