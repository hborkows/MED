from utils.item import Item


def find_node_r(node: Item, name: str):
    if node.name == name:
        return node
    elif node.children:
        for child in node.children:
            result = find_node_r(child, name)
            if result:
                return result
        return None
    else:
        return None


def get_ancestors_r(node: Item):
    if node.parent:
        result = [node]
        parent_ancestors = get_ancestors_r(node.parent)
        if parent_ancestors:
            result += parent_ancestors
        return result
    else:
        return None


class Taxonomy:
    def __init__(self):
        self._root = Item(name='__root__', parent=None)

    def find_node(self, name: str):
        return find_node_r(self._root, name)

    def add_node(self, node_name: str, parent_name: str):
        parent = self.find_node(parent_name)
        node = Item(name=node_name, parent=parent)
        parent.add_child(node)

    def get_ancestors(self, node: Item):
        return get_ancestors_r(node.parent)
