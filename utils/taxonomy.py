from utils.item import Item


def find_node_r(node: Item, node_id: str):
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
        self._root: Item = Item(node_id='__root__', parent=None)

    def find_node(self, node_id: str):
        return find_node_r(self._root, node_id)

    def add_node(self, node_id: str, parent_id: str, node_description: str = ''):
        parent = self.find_node(parent_id)
        node = Item(node_id=node_id, parent=parent, desc=node_description)
        parent.add_child(node)

    def get_ancestors(self, node: Item):
        return get_ancestors_r(node.parent)
