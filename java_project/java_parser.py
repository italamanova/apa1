import os

import javalang
import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')
from graphviz import Digraph
from javalang.tree import MethodInvocation, VariableDeclaration, VariableDeclarator, ClassDeclaration, \
    MethodDeclaration, Import, PackageDeclaration, ConstructorDeclaration, IfStatement, WhileStatement, ForStatement, \
    ClassCreator


############## BASIC STRUCTURE ################
class Package:
    def __init__(self, _name):
        self.name = _name

    def __str__(self):
        return 'Package %s' % (self.name)
        # return self.name

    def __repr__(self):
        return 'Package %s Classes: %s' % (self.name, self.classes)
        # return self.name


class Class:
    def __init__(self, _name, extends=None, implements=None):
        self.name = _name
        self.extends = extends
        self.implements = implements
        self.methods = []

    def __str__(self):
        return 'Class %s Methods: %s\n' % (self.name, self.methods)
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

    def get_children(self, classes):
        children = []
        for class_instance in classes:
            if class_instance.extends == self.name:
                children.append(class_instance)
        return children


class Method:
    def __init__(self, name, params, class_name=None):
        self.name = name
        self.params = params
        self.class_name = class_name
        self.calls = []

    def __str__(self):
        return 'Method %s.%s, Calls: %s' % (self.class_name, self.name, self.calls)

    def __repr__(self):
        return 'Method %s.%s, Calls: %s' % (self.class_name, self.name, self.calls)

    @property
    def pretty_name(self):
        return '%s.%s' % (self.class_name, self.name)

    def add_call(self, call):
        if call not in self.calls:
            self.calls.append(call)

    def is_equal(self, method_call_name):
        return method_call_name == self.name


class Call:
    def __init__(self, name, qualifier, class_name=None):
        self.name = name
        self.qualifier = qualifier
        self.class_name = class_name

    def __str__(self):
        if self.class_name:
            return '%s.%s' % (self.class_name, self.name)
        return '%s' % self.name

    def __repr__(self):
        if self.class_name:
            return '%s.%s' % (self.class_name, self.name)
        return '%s' % self.name

    @property
    def pretty_name(self):
        if self.class_name:
            return '%s.%s' % (self.class_name, self.name)
        return '%s' % self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash("call" * len(self.name))


class Variable:
    def __init__(self, _name, _type):
        self.name = _name
        self.type = _type

    def __str__(self):
        return '%s %s' % (self.type, self.name)

    def __repr__(self):
        return '%s %s' % (self.type, self.name)


############## DRAWER ################
def draw_graph(graph_file_path, edges_dict):
    name = 'pictures/graph.gv'
    g = Digraph('G', filename=name)
    for parent in edges_dict:
        for child in edges_dict.get(parent):
            g.edge(parent.name, child.name)
    g.view()


def draw_call_graph(call_graph_list):
    name = 'pictures/call_graph.gv'
    g = Digraph('G', filename=name)
    for node in call_graph_list:
        g.edge('%s' % node[0], '%s' % node[1])
    g.view()


def draw_plot(wmc, rfc):
    fig = plt.figure()

    for key, value in wmc.items():
        x = value
        y = rfc[key]
        plt.plot(x, y, 'bo')
        plt.text(x * (1 + 0.02), y * (1 + 0.02), key, fontsize=8)

    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    plt.xlabel('WMC')
    plt.ylabel('RFC')
    plt.title('Metrics')
    fig.savefig('pictures/plot.png')


file_structure = []
all_methods = []

call_graph = {}


### HELPERS ###

def get_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            return data
    except OSError as e:
        return None


def find_in_list(f, seq):
    for item in seq:
        if f(item):
            return item


### HELPERS FOR PARSING ###

def get_parent_folder(folder_path):
    parent_folder = os.path.abspath(os.path.join(folder_path, os.pardir))
    if not parent_folder == '/':
        return parent_folder
    else:
        return None


def add_parent_class_methods(classes):
    pass
    # for class_instance in classes:
    #     print(class_instance.name, class_instance.extends)
    # if class_instance.extends:
    #     parent = find_in_list(lambda item: item.name == class_instance.extends, classes)
    #     for method in parent.methods:
    #         child_method = Method(method.name, method.params, class_name=class_instance)
    #         child_method.calls = method.calls
    #         class_instance.add_method(child_method)


def find_call_type(variable_list, qualifier):
    variable = variable_list.get(qualifier)
    if hasattr(variable, 'type'):
        return variable.type
    return None


def has_nested_children(node):
    types = [IfStatement, ForStatement, WhileStatement]
    has_nested = False
    if type(node) in types:
        for inner_path, inner_node in node:
            if type(inner_node) in types:
                has_nested = True
    return has_nested


def count_nested(node):
    maximum = 0
    for inner_path, inner_node in node:
        if inner_path:
            if isinstance(inner_node, IfStatement) or isinstance(inner_node, ForStatement) \
                    or isinstance(inner_node, WhileStatement):
                current = 1
                if has_nested_children(inner_node):
                    current += count_nested(inner_node)

                if current > maximum:
                    maximum = current
    return maximum


def count_response(classes):
    responses = {}
    for class_instance in classes:
        class_counter = 0
        for method in class_instance.methods:
            class_counter += 1
            for call in method.calls:
                class_counter += 1
        responses.update({class_instance.name: class_counter})
    return responses


def build_file_structure(file_path, project_classes, count_wmc, package_start=None):
    data = get_file(file_path)
    if data:
        tree = javalang.parse.parse(data)

        imports = []
        classes = []
        variables = {}

        for tree_path, tree_node in tree:
            if isinstance(tree_node, VariableDeclaration):
                for var_path, var_node in tree_node:
                    if isinstance(var_node, VariableDeclarator):
                        try:
                            variable = Variable(var_node.name, tree_node.type.name)
                            variables.update({var_node.name: variable})
                        except Exception:
                            pass

        for path, node in tree:
            if isinstance(node, PackageDeclaration):
                main_package = node.name

            if isinstance(node, Import):
                imports.append(node.path)

            if isinstance(node, ClassDeclaration):
                class_instance = Class(node.name, node.extends)
                if node.extends:
                    class_instance.extends = node.extends.name

                if node.implements:
                    # print('implements', node.implements[0].name)
                    class_instance.implements = node.implements[0].name

                classes.append(class_instance)

                for class_child in node.body:
                    if isinstance(class_child, MethodDeclaration):
                        method = Method(class_child.name, class_child.parameters, class_name=node.name)
                        class_instance.add_method(method)
                        for method_path, method_node in class_child:
                            if isinstance(method_node, MethodInvocation):
                                call_class_name = find_call_type(variables, method_node.qualifier)
                                if call_class_name:
                                    method_call = Call(method_node.member, method_node.qualifier,
                                                       class_name=call_class_name)
                                else:
                                    method_call = Call(method_node.member, method_node.qualifier,
                                                       class_name=class_instance.name)

                                method.add_call(method_call)
                            if isinstance(method_node, ClassCreator):
                                method_call = Call('new', None,
                                                   class_name=method_node.type.name)
                                method.add_call(method_call)

                    if isinstance(class_child, ConstructorDeclaration):
                        method = Method('new', class_child.parameters, class_name=node.name)
                        class_instance.add_method(method)
                        for constructor_path, constructor_node in class_child:
                            if isinstance(constructor_node, MethodInvocation):
                                if constructor_node.qualifier:
                                    call_class_name = find_call_type(variables, constructor_node.qualifier)
                                    method_call = Call(constructor_node.member, constructor_node.qualifier,
                                                       class_name=call_class_name)
                                else:
                                    method_call = Call(constructor_node.member, None,
                                                       class_name=class_instance.name)
                                method.add_call(method_call)

                            if isinstance(constructor_node, ClassCreator):
                                method_call = Call('new', None,
                                                   class_name=constructor_node.type.name)
                                method.add_call(method_call)

                    if isinstance(class_child, ConstructorDeclaration) or isinstance(class_child, MethodDeclaration):
                        # COUNT WMC
                        method_lnd = count_nested(class_child)
                        if count_wmc.get(class_instance.name):
                            count_wmc[class_instance.name] += method_lnd
                        else:
                            count_wmc.update({class_instance.name: method_lnd})
        project_classes += classes

        if package_start:
            folder_path = '/'.join(file_path.split('/')[:-1])
            folder_parent_path = folder_path[:package_start]
            for _import in imports:

                import_name = _import.split('.')[-1]
                check_import = find_in_list(lambda item: item.name == import_name, project_classes)

                if not check_import:
                    import_path = '/'.join(_import.split('.'))
                    import_file = '%s%s.java' % (folder_parent_path, import_path)
                    build_file_structure(import_file, project_classes, count_wmc, package_start)

        return main_package, imports
    else:
        return None, None


def build_project_structure(main_file_path):
    main_folder_path = '/'.join(_file_path.split('/')[:-1])
    project_classes = []
    count_wmc = {}
    main_package, main_file_imports = build_file_structure(main_file_path, project_classes, count_wmc)
    package_start = main_folder_path.find('/'.join(main_package.split('.')))
    main_folder_parent_path = main_folder_path[:package_start]
    for _import in main_file_imports:
        import_path = '/'.join(_import.split('.'))
        import_file = '%s%s.java' % (main_folder_parent_path, import_path)
        build_file_structure(import_file, project_classes, count_wmc, package_start=package_start)
    add_parent_class_methods(project_classes)
    return project_classes, count_wmc


def get_methods_recursively(method_instance, classes, graph_call):
    if method_instance.calls:
        for call in method_instance.calls:
            graph_call.append([method_instance.pretty_name, call.pretty_name])
            call_class_name = call.class_name
            call_method_name = call.name
            for class_instance in classes:
                if class_instance.name == call_class_name:
                    for method in class_instance.methods:
                        if method.name == call_method_name:
                            get_methods_recursively(method, classes, graph_call)


def prepare_call_graph(proj_classes):
    graph_call = []
    # TODO: need to draw
    for class_instance in project_classes:
        if class_instance.get_method('main'):
            main_method = class_instance.get_method('main')
            get_methods_recursively(main_method, proj_classes, graph_call)

    draw_call_graph(graph_call)


var = input("Please enter file path: ")
print("File path: " + str(var))
_file_path = str(var)
project_classes, count_wmc = build_project_structure(_file_path)
for item in project_classes:
    print(item)
count_rfc = count_response(project_classes)

print('WMC', count_wmc)
print('RFC', count_rfc)

draw_plot(count_wmc, count_rfc)

prepare_call_graph(project_classes)
