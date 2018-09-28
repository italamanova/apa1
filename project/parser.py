import ast
import re

from project.basic_structures import Analysis, Class, Method
from tests import a2

hierarchy = {}

file_structure = []
all_methods = []

call_graph = {}


def get_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        return data


def get_main_function(_source):
    pattern = r'if __name__ == \'__main__\'\:\s*(.+)$'
    match = re.findall(pattern, _source)[0]
    splitted_match = match.split('.')

    if len(splitted_match) < 2:
        class_name = None
        main_method_name = re.findall(r'(\w+)\(', splitted_match[0])
    else:
        class_name = re.findall(r'(\w+)\(', splitted_match[0])[0]
        main_method_name = re.findall(r'(\w+)\(', splitted_match[1])[0]

    return class_name, main_method_name


class NodeVisitor(ast.NodeVisitor):

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
            if parent_class in hierarchy:
                hierarchy.get(parent_class).append(child_class)
            else:
                hierarchy.update({parent_class: [child_class]})

        current_class = Class(child)

        for function_item in ast.iter_child_nodes(tree):
            if isinstance(function_item, ast.FunctionDef):
                current_method = Method(function_item.name, function_item.args)
                current_class.add_method(current_method)

                for node in ast.walk(function_item):
                    if isinstance(node, ast.Call):
                        func = node.func
                        if isinstance(func, ast.Name):
                            # print('name', func.id)
                            current_method.add_call(func.id)

                        if isinstance(func, ast.Attribute):
                            if isinstance(func.value, ast.Call):
                                # print('another call', func.value, func.attr)
                                current_method.add_call(func.attr)
                            else:
                                # print('attr', func.value.id, func.attr)
                                current_method.add_call(func.attr)

        file_structure.append(current_class)


def walk_file_structure(method_name):
    for i, class_item in enumerate(file_structure):
        for method_item in class_item.methods:
            if method_item.name == method_name:
                _method = file_structure[i].get_method(method_name)
                call_graph.update({method_name: _method.calls})
                for call_name in _method.calls:
                    walk_file_structure(call_name)


file = get_file('/home/talamash/PycharmProjects/apa1/tests/a2.py')
tree = ast.parse(get_file('/home/talamash/PycharmProjects/apa1/tests/a2.py'))

print(ast.dump(tree))
NodeVisitor().visit(tree)

main_class_name, main_method_name = get_main_function(file)

for i, class_item in enumerate(file_structure):
    if main_method_name:
        if class_item.name == main_class_name:
            for method_item in class_item.methods:
                if method_item.name == main_method_name:
                    main_method = file_structure[i].get_method(main_method_name)
                    print('CALLS', main_method.calls)
                    call_graph.update({main_method_name: main_method.calls})
                    for method_call_name in main_method.calls:
                        walk_file_structure(method_call_name)

        else:
            # check function without class
            pass

analysis = Analysis(a2, hierarchy)

# draw_graph('', hierarchy)

print(call_graph)
