import inspect

from project.basic_structures import Analysis, Method
from project.drawer import draw_graph
from project.function_parser import get_main_function
from tests import a2

analysis = Analysis(a2)


def draw_classes():
    hierarchy = analysis.hierarchy
    # print(hierarchy)
    draw_graph('', hierarchy)


def get_methods():
    file = analysis.file
    main_class_name, main_method_name = get_main_function(file)

    hierarchy = analysis.hierarchy
    print('hierarchy', hierarchy)
    instance_dict = {}
    simple_instance_dict = {}
    classes = inspect.getmembers(file, predicate=inspect.isclass)

    for instance_name, instance in classes:
        # print(111,
        #       [attr for attr in dir(instance) if not callable(getattr(instance, attr)) and not attr.startswith("__")])

        class_functions = inspect.getmembers(instance, predicate=inspect.isfunction)
        class_methods = inspect.getmembers(instance, predicate=inspect.ismethod)
        all_class_methods = class_functions + class_methods
        method_list = [Method(current_method_name, method_instance) for current_method_name, method_instance in
                       all_class_methods]

        instance_dict.update({instance_name: method_list})
        # simple_instance_dict.update(
        #     {instance_name: [current_method_name for current_method_name, method_instance in all_class_methods]})

        for method in method_list:
            method.get_variables()
            # calls = method.find_calls()
            # print('called_methods', calls)
    print('instance_dict', instance_dict)
    # if main_class_name:
    #     main_class_methods = instance_dict.get(main_class_name)
    #     main_method = [item for item in main_class_methods if main_method_name in item]
    #     calls = find_calls(main_method[0][1])
    #     print('calls', calls)
    #     check_calls(calls, instance_dict)
    #     #recursively call for each method

    # else:
    #     # handle function without class
    #     pass

    # print('class: ', instance.__name__)
    # print('class_members: ', class_functions)
    # print()
    # print('---', simple_instance_dict)


def draw_call_graph():
    pass


# draw_classes(a2)
get_methods()

# print(dir(a2.itertools))

# hierarchy = get_class_hierarchy(a2)
# print(hierarchy)
# print(get_children('B', hierarchy))
# print(get_parents('B', a2))
