from utils.item import Item


def find_node_r(node: Item, node_id: int):
    if node.node_id == node_id:
        return node
    elif node.children:
        for child in node.children:
            result = find_node_r(child, node_id)
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
        self._root: Item = Item(node_id=-1, parent=None)

    def find_node(self, node_id: int):
        return find_node_r(self._root, node_id)

    def add_node(self, node_id: int, parent_id: int, node_description: str = ''):
        parent = self.find_node(parent_id)
        node = Item(node_id=node_id, parent=parent, desc=node_description)
        parent.add_child(node)

    def get_ancestors(self, node: Item):
        return get_ancestors_r(node.parent)

    def _print_r(self, node: Item, indent: str):
        node.print(indent)
        indent = indent + '  '
        for child in node.children:
            self._print_r(child, indent)

    def print(self):
        self._print_r(self._root, indent='')
