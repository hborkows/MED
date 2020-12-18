from utils.taxonomy import Taxonomy
from utils.item import Item
import re
import pandas as pd


def filter_string_list(string_list: list, regex_string: str, negative_regex: bool = False) -> list:
    regex = re.compile(regex_string)
    if negative_regex:
        return [string for string in string_list if not regex.match(string)]
    else:
        return [string for string in string_list if regex.match(string)]


def read_item_list(path: str) -> dict:
    with open(path, 'r') as file:
        lines = file.readlines()
    filtered_lines = filter_string_list(lines, regex_string='^@ITEM.*\n$')
    
    item_dict = {}
    for line in filtered_lines:
        item_id = line[6:10]
        item_name = line[11:-1]
        item_dict[item_id] = item_name
    
    return item_dict
    

def read_transactions(path: str, taxonomy: Taxonomy) -> list:
    with open(path, 'r') as file:
        lines = file.readlines()
    filtered_lines = filter_string_list(lines, regex_string='^@ITEM.*\n$', negative_regex=True)

    transactions = []
    for line in filtered_lines:
        item_ids = line[:-1].split(' ')
        transaction = []
        for node_id in item_ids:
            transaction.append(taxonomy.find_node(node_id=node_id))
        transactions.append(transaction)

    return transactions
        

def add_nodes_r(node: Item, taxonomy_df: pd.DataFrame, taxonomy: Taxonomy, items: dict):
    relevant_data = taxonomy_df[taxonomy_df['parent'] == node.node_id]
    children = relevant_data['child'].tolist()
    for child in children:
        try:
            description = items[child]
        except KeyError:
            description = ''
        taxonomy.add_node(node_id=child, parent_id=node.node_id, node_description=description)
        add_nodes_r(taxonomy.find_node(node_id=child), taxonomy_df, taxonomy, items)


def read_taxonomy(path: str, items: dict) -> Taxonomy:
    taxonomy = Taxonomy()

    tax_df = pd.read_csv(path)
    parents = set(list(tax_df['parent']))
    children = set(list(tax_df['child']))

    # Generate top level taxonomy nodes
    top_parents = parents - children
    parent_id = '__root__'
    for parent in top_parents:
        try:
            description = items[parent]
        except KeyError:
            description = ''
        taxonomy.add_node(node_id=parent, parent_id=parent_id, node_description=description)
        # Recursively add lower level nodes
        add_nodes_r(node=taxonomy.find_node(node_id=parent), taxonomy_df=tax_df, taxonomy=taxonomy, items=items)

    return taxonomy


if __name__ == '__main__':
    print(read_item_list('../data/fruithut_original.txt'))
