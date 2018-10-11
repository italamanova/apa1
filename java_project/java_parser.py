import os

import javalang
from javalang.tree import MethodInvocation, VariableDeclaration, VariableDeclarator, ClassDeclaration, \
    MethodDeclaration, Import, PackageDeclaration, ConstructorDeclaration, IfStatement, WhileStatement, ForStatement

from java_project.java_basic_structures import Variable, Class, Method, Call

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


def build_file_structure(file_path, project_classes):
    data = get_file(file_path)
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
                print('extends', class_instance.extends)

            if node.implements:
                class_instance.implements = node.implements.name
                print('impl', class_instance.implements)

            classes.append(class_instance)

            for class_child in node.body:
                if isinstance(class_child, MethodDeclaration):
                    method = Method(class_child.name, class_child.parameters, class_name=node.name)
                    class_instance.add_method(method)
                    for method_path, method_node in class_child:
                        if isinstance(method_node, MethodInvocation):
                            # print('CLASS', class_instance.name)
                            call_class_name = find_call_type(variables, method_node.qualifier)
                            method_call = Call(method_node.member, method_node.qualifier, class_name=call_class_name)
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

                # COUNT LND
                if isinstance(class_child, ConstructorDeclaration) or isinstance(class_child, MethodDeclaration):

                    lnd = count_nested(class_child)
                    print(class_child.name, lnd)

    project_classes += classes
    return main_package, imports


def build_project_structure(main_file_path):
    main_folder_path = '/'.join(_file_path.split('/')[:-1])
    project_classes = []
    main_package, main_file_imports = build_file_structure(main_file_path, project_classes)
    package_start = main_folder_path.find('/'.join(main_package.split('.')))
    main_folder_parent_path = main_folder_path[:package_start]
    for _import in main_file_imports:
        import_path = '/'.join(_import.split('.'))
        import_file = '%s%s.java' % (main_folder_parent_path, import_path)
        build_file_structure(import_file, project_classes)
    return project_classes


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


def draw_call_graph(project_classes):
    graph_call = []
    # TODO: need to draw
    for class_instance in project_classes:
        if class_instance.get_method('main'):
            main_method = class_instance.get_method('main')
            get_methods_recursively(main_method, project_classes, graph_call)

    print(graph_call)


_file_path = "/home/talamash/workspace/test_project/src/package2/FlightSim1.java"
# _file_path = "/home/talamash/workspace/test_project/src/package1/Panel.java"
project_classes = build_project_structure(_file_path)
print('project_classes', project_classes)

# print('count_response', count_response(project_classes))

draw_call_graph(project_classes)
