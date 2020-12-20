class Item:
    def __init__(self, node_id: str, parent, desc: str = ''):
        self.node_id: str = node_id
        self.parent = parent
        self.desc: str = desc
        self.children: list = []

    def add_child(self, child):
        self.children.append(child)

    def print(self, indent: str):
        print(indent + str(self.node_id))
