import ast
import inspect
import re

from graphviz import Digraph

from project.basic_structures import Class, Function, FunctionCall

file_structure = []
all_methods = []

call_graph = {}


def get_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        return data


class FileStructureVisitor(ast.NodeVisitor):

    def __init__(self):
        super(FileStructureVisitor, self).__init__()
        self.hierarchy = {}
        self.all_calls = []

    def handle_FunctionDef(self, function_item, class_instance):
        current_function = Function(function_item.name, function_item.args)
        if class_instance:
            current_function.class_name = class_instance.name
        for node in ast.walk(function_item):

            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name):
                    # print('name', func.id)
                    current_function.add_call(FunctionCall(func.id))

                if isinstance(func, ast.Attribute):
                    if isinstance(func.value, ast.Call):
                        current_function.add_call(FunctionCall(func.attr))
                    else:
                        # print('attr', func.value.id, func.attr)
                        current_function.add_call(FunctionCall(func.attr))
        return current_function

    # def visit_Import(self, tree_node):
    #     print('import', tree_node.names)
    #     for item in tree_node.names:
    #         print(item.name)
    #         module_instance = sys.modules[item.name]
    #         for attr_name in dir(module_instance):
    #             attr_instance = getattr(module_instance, attr_name)
    #             print('attr_instance', attr_instance)
    #
    #             # source_file = inspect.getsource(attr_instance)
    #             # print('source_file', source_file)
    #             # NodeVisitor().visit(source_file)
    #         # print('MODULE', dir(module_instance))
    #     self.generic_visit(tree_node)

    def visit_ClassDef(self, tree):
        child = tree.name
        parents = tree.bases
        child_class = Class(child)
        for parent in parents:
            parent_name = parent.id
            parent_class = Class(parent_name)
            if parent_class in self.hierarchy:
                self.hierarchy.get(parent_class).append(child_class)
            else:
                self.hierarchy.update({parent_class: [child_class]})

        current_class = Class(child)
        for function_item in ast.iter_child_nodes(tree):
            if isinstance(function_item, ast.FunctionDef):
                fuction_instance = self.handle_FunctionDef(function_item, current_class)
                current_class.add_method(fuction_instance)

        file_structure.append(current_class)

        self.generic_visit(tree)

    def visit_Call(self, tree):
        func = tree.func
        if isinstance(func, ast.Name):
            self.all_calls.append(func.id)

        if isinstance(func, ast.Attribute):
            self.all_calls.append(func.attr)


def get_main_function(_source):
    pattern = r'if __name__ == (\'|\")__main__(\'|\")\:\s*(.+)$'
    match = re.findall(pattern, _source)
    try:
        main_names = match[0][2]
    except IndexError:
        return None

    splitted_match = main_names.split('.')

    if len(splitted_match) < 2:
        class_name = None
        main_method_name = re.findall(r'(\w+)\(', splitted_match[0])[0]
    else:
        class_name = re.findall(r'(\w+)\(', splitted_match[0])[0]
        main_method_name = re.findall(r'(\w+)\(', splitted_match[1])[0]

    return class_name, main_method_name


def find_call_classes(all_calls, current_file_structure):
    for call_name in all_calls:
        for class_item in current_file_structure:
            if isinstance(class_item, Class):
                class_instance = class_item.get_call_class(call_name)
                if class_instance:
                    for call_class_item in current_file_structure:
                        if call_class_item.name == class_instance.name:
                            call_class_item.set_call_class(call_name, call_class_item)

    return current_file_structure


def walk_file_structure(method_name, _file_structure):
    for i, file_structure_item in enumerate(_file_structure):
        if isinstance(file_structure_item, Class):
            for method_item in file_structure_item.methods:
                if method_item.name == method_name:
                    _method = _file_structure[i].get_method(method_name)
                    call_graph.update({method_name: _method.calls})
                    for call in _method.calls:
                        walk_file_structure(call.name, _file_structure)
        elif isinstance(file_structure_item, Function):
            if file_structure_item.name == method_name:
                _function = _file_structure[i]
                call_graph.update({method_name: _function.calls})
                for call in _function.calls:
                    walk_file_structure(call.name, _file_structure)


def prepare_graph_data(file_path):
    source_file = get_file(file_path)
    tree = ast.parse(source_file)

    # create file structure
    file_structure_visitor = FileStructureVisitor()
    file_structure_visitor.visit(tree)

    for direct_child in ast.iter_child_nodes(tree):
        if not isinstance(direct_child, ast.ClassDef):
            for node in ast.walk(direct_child):
                if isinstance(node, ast.FunctionDef):
                    outside_function = file_structure_visitor.handle_FunctionDef(node, None)
                    file_structure.append(outside_function)

    print('file_structure', file_structure)

    all_calls = file_structure_visitor.all_calls

    # create call graph

    _main = get_main_function(source_file)
    if _main:
        main_class_name, main_method_name = get_main_function(source_file)

        for i, file_structure_item in enumerate(file_structure):

            if main_class_name:
                if file_structure_item.name == main_class_name:
                    for method_item in file_structure_item.methods:
                        if method_item.name == main_method_name:
                            main_method = file_structure[i].get_method(main_method_name)
                            call_graph.update({main_method_name: main_method.calls})
                            for method_call in main_method.calls:
                                walk_file_structure(method_call.name, file_structure)

            else:
                if file_structure_item.name == main_method_name:
                    main_function = file_structure[i]
                    call_graph.update({main_method_name: main_function.calls})
                    for method_call in main_function.calls:
                        walk_file_structure(method_call.name, file_structure)

    hierarchy = file_structure_visitor.hierarchy
    return hierarchy, call_graph


# print(file_structure)

# var = input("Please enter file path: ")
# print("File path: " + str(var))
# hierarchy, the_call_graph = prepare_graph_data(str(var))
# draw_call_graph('', the_call_graph)
# draw_graph('', hierarchy)


import javalang
tree = javalang.parse.parse("package javalang.brewtab.com; class Test {}")
print(tree.children)
