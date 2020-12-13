class Item:
    def __init__(self, name):
        self.name = name
        self._children = []

    def add_child(self, child):
        self._children.append(child)

    def get_children(self):
        return self._children
