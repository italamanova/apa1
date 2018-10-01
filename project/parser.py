import ast
import inspect
import re

from graphviz import Digraph

file_structure = []
all_methods = []

call_graph = {}


#### BASIC STRUCTURES #####


class Analysis:
    def __init__(self, _file, _hierarchy):
        self.file = _file
        self.hierarchy = _hierarchy

    def get_children(self, class_name):
        children = []
        for item in self.hierarchy:
            if item.name == class_name:
                children += self.hierarchy.get(item)
                for child in self.hierarchy.get(item):
                    deep_children_search = self.get_children(child.name, self.hierarchy)
                    if deep_children_search:
                        children += deep_children_search
        return children

    def get_parents(self, class_name):
        class_instance = getattr(self.file, class_name)
        mro = list(inspect.getmro(class_instance))[1:-1]
        return mro


class Class:
    def __init__(self, _name):
        self.name = _name
        self.methods = []

    def __str__(self):
        return 'Class %s Methods: %s' % (self.name, self.methods)
        # return self.name

    def __repr__(self):
        return 'Class %s Methods: %s' % (self.name, self.methods)
        # return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash("foobar" * len(self.name))

    def add_method(self, method):
        if method not in self.methods:
            self.methods.append(method)

    def get_method(self, method_name):
        for method in self.methods:
            if method.name == method_name:
                return method
        return None

    def get_call_class(self, call_instance_name):
        for method in self.methods:
            if method.name == call_instance_name:
                return self

    def set_call_class(self, call_name, class_instance):
        for method in self.methods:
            for call in method.calls:
                if call.name == call_name:
                    call.set_class_name(class_instance.name)


class Function:
    def __init__(self, _name, _params):
        self.name = _name
        self.class_name = None
        self.params = _params
        self.calls = []

    def __str__(self):
        return 'Function %s.%s, Calls: %s' % (self.class_name, self.name, self.calls)

    def __repr__(self):
        return 'Function %s.%s, Calls: %s' % (self.class_name, self.name, self.calls)

    def add_call(self, call):
        if call not in self.calls:
            self.calls.append(call)

    def is_equal(self, method_call_name):
        return method_call_name == self.name


class FunctionCall:
    def __init__(self, _name):
        self.name = _name
        self.class_name = None

    def __str__(self):
        return '%s' % (self.name)

    def __repr__(self):
        return '%s' % (self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash("finctioncall" * len(self.name))

    def set_class_name(self, _class_name):
        self.class_name = _class_name


#### DRAWING #####


def draw_graph(graph_file_path, edges_dict):
    name = 'pictures/graph.gv'
    g = Digraph('G', filename=name)
    for parent in edges_dict:
        for child in edges_dict.get(parent):
            g.edge(parent.name, child.name)
    g.view()


def draw_call_graph(graph_file_path, call_graph_dict):
    name = 'pictures/call_graph.gv'
    g = Digraph('G', filename=name)
    for node in call_graph_dict:
        for node_child in call_graph_dict.get(node):
            g.edge('%s()' % node, '%s()' % node_child)
    g.view()


#### PARSING #####


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

var = input("Please enter file path: ")
print("File path: " + str(var))
hierarchy, the_call_graph = prepare_graph_data(str(var))
draw_call_graph('', the_call_graph)
draw_graph('', hierarchy)
