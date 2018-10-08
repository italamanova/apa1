import os

import javalang
from javalang.tree import MethodInvocation, VariableDeclaration, VariableDeclarator, ClassDeclaration, \
    MethodDeclaration, Import

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


def get_subfolder(entry_folder_path, subfolder_name):
    files = os.listdir(entry_folder_path)
    for name in files:
        if name == subfolder_name:
            return '/'.join([entry_folder_path, name])
        # else:
        #     print('name !=', name)
        #     parent_path = get_parent_folder(entry_folder_path)
        #     get_subfolder(parent_path, subfolder_name)
    return None


def get_import_file(import_path_list, main_folder_path):
    parent_dir = get_parent_folder(main_folder_path)
    import_folder_path = get_subfolder(parent_dir, import_path_list[0])
    return import_folder_path


def find_call_type(variable_list, qualifier):
    variable = variable_list.get(qualifier)
    if hasattr(variable, 'type'):
        return variable.type
    return None


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
    print('variables', variables)

    for path, node in tree:

        if isinstance(node, Import):
            imports.append(node.path)

        if isinstance(node, ClassDeclaration):
            class_instance = Class(node.name, node.extends)
            classes.append(class_instance)

            # print('constructors', node.constructors)
            # print('extends', node.extends)
            # print(dir(node))

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
        #                    check call params
    #
    #     # if isinstance(node, FormalParameter):
    #     #     print(node)
    #     #     print(node.name)
    #     #     print(node.type)
    #     #
    #     # if isinstance(node, ReferenceType):
    #     #     print(node)
    #     #     print(node.name)
    #
    # print(classes)
    project_classes += classes
    return imports


def build_project_structure(main_file_path):
    main_folder_path = '/'.join(_file_path.split('/')[:-1])
    project_classes = []
    main_file_imports = build_file_structure(main_file_path, project_classes)
    for _import in main_file_imports:
        import_path_list = _import.split('.')
        import_folder_path = get_import_file(import_path_list, main_folder_path)
        # TODO: change import search
        import_file = '/'.join([import_folder_path, '%s.java' % import_path_list[1]])
        # build_file_structure(import_file, project_classes)
    print('project_classes', project_classes)

folder_path = "/home/talamash/workspace/test_project/src/package2"

# _file_path = "/home/talamash/workspace/test_project/src/package2/FlightSim.java"
_file_path = "/home/talamash/workspace/test_project/src/package1/Panel.java"
build_project_structure(_file_path)
