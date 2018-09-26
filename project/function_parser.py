import inspect
import re

from tests import a2


# def explode(s):
#     pattern = r'(\w[\w\d_]*)\((.*)\)$'
#     match = re.match(pattern, s)
#     if match:
#         return list(match.groups())
#     else:
#         return []

def get_main_function(file):
    _source = inspect.getsource(file)
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


def find_calls(method_instance):
    print('method_instance', method_instance)
    method_source = inspect.getsource(method_instance)
    all_calls = re.findall(r'(\w+)\(', method_source)
    return all_calls[1:]


def check_calls(method_calls, instance_dict):
    print(111, method_calls, instance_dict)
    classes_with_method = {}
    for call in method_calls:
        if call in instance_dict:
            pass
            # create __new__ node
        else:
            for class_name in instance_dict:
                class_methods = instance_dict.get(class_name)
                for method in class_methods:
                    if call in method:
                        classes_with_method.update({class_name: call})
                    calls = find_calls(method[1])
                    _classes = check_calls(calls, instance_dict)

                    classes_with_method.update(_classes)
            return classes_with_method


print(get_main_function(a2))
