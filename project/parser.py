import ast
import inspect
import sys

from project.basic_structures import Analysis
from project.drawer import draw_graph
from tests import a2

hierarchy = {}


def get_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        return data


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
    #
    def visit_ClassDef(self, tree_node):
        child = tree_node.name
        parents = tree_node.bases

        for parent in parents:
            parent_name = parent.id
            if parent_name in hierarchy:
                hierarchy.get(parent_name).append(child)
            else:
                hierarchy.update({parent_name: [child]})

        print('class', child)

        self.generic_visit(tree_node)

    def visit_FunctionDef(self, tree_node):
        print('func', tree_node.name, tree_node.args)
        self.generic_visit(tree_node)

    def visit_Call(self, tree_node):
        func = tree_node.func
        if isinstance(func, ast.Name):
            print('name', func.id)

        if isinstance(func, ast.Attribute):
            if isinstance(func.value, ast.Call):
                print('another call', func.value, func.attr)
            else:
                print('attr', func.value.id, func.attr)



tree = ast.parse(get_file('/home/talamash/PycharmProjects/apa1/tests/a2.py'))

print(ast.dump(tree))
NodeVisitor().visit(tree)

print('hierarchy', hierarchy)
analysis = Analysis(a2, hierarchy)



# draw_graph('', hierarchy)
