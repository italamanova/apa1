import os

import javalang
from javalang.tree import ClassDeclaration, MethodDeclaration, FormalParameter, ReferenceType

from java_project.java_basic_structures import Class, Method

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


def build_file_structure(file_path):
    data = get_file(file_path)
    tree = javalang.parse.parse(data)

    imports = []
    classes = []

    for path, node in tree:
        print(node)
        # if isinstance(node, Import):
        #     print(node)
        #     print(dir(node))
        #
        #     path_list = node.path.split('.')
        #     print(path_list)

        # if isinstance(node, ClassDeclaration):
        #     print('class', node)
        #     class_instance = Class(node.name, node.extends)
        #     classes.append(class_instance)
        #
        #     # print('constructors', node.constructors)
        #     # print('methods', node.methods)
        #     # print('extends', node.extends)
        #
        #     for class_child in node.body:
        #
        #         if isinstance(class_child, MethodDeclaration):
        #             # print('method', class_child)
        #             # print('method dir', dir(class_child))
        #             method = Method(class_child.name, class_child.parameters)
        #             class_instance.add_method(method)
        #
        # if isinstance(node, FormalParameter):
        #     print(node)
        #     print(node.name)
        #     print(node.type)
        #
        # if isinstance(node, ReferenceType):
        #     print(node)
        #     print(node.name)
    # print(classes)


# folder_path = "/home/talamash/workspace/test_project/src/package2"
# parent_path = get_parent_folder(folder_path)
# print(check_subfolders(parent_path, 'package2'))

_file_path = "/home/talamash/workspace/test_project/src/package2/FlightSim.java"
build_file_structure(_file_path)
