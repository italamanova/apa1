import os

import javalang

file_structure = []
all_methods = []

call_graph = {}


def get_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        return data


def get_parent_folder(folder_path):
    parent_folder = os.path.abspath(os.path.join(folder_path, os.pardir))
    if not parent_folder == '/':
        return parent_folder
    else:
        return None


def check_subfolders(folder_path, check_name):
    files = os.listdir(folder_path)
    for name in files:
        if name == check_name:
            return name
    return None


def print_children(tree):
    if tree:
        print('TREE', tree)
        try:
            for child in tree.children:
                print(child)
                child_tree = child
                print_children(child_tree)
        except:
            print(tree)


_file_path = "/home/talamash/workspace/test_project/src/package2/FlightSim.java"
data = get_file(_file_path)
tree = javalang.parse.parse(data)
# for path, node in tree:
#     # print(node)
#     if isinstance(node, Import):
#         print(node)
#         print(dir(node))
#
#         path_list = node.path.split('.')
#         print(path_list)

# if isinstance(node, ClassDeclaration):
#     print(node)
#     # print(dir(node))
#     print('constructors', node.constructors)
#     print('methods', node.methods)
#     print('extends', node.extends)
#
# if isinstance(node, MethodDeclaration):
#     print(node)
#     print(node.name)
#     print(node.parameters)
#
# if isinstance(node, FormalParameter):
#     print(node)
#     print(node.name)
#     print(node.type)
#
# if isinstance(node, ReferenceType):
#     print(node)
#     print(node.name)


folder_path = "/home/talamash/workspace/test_project/src/package2"

parent_path = get_parent_folder(folder_path)

print(check_subfolders(parent_path, 'package2'))

