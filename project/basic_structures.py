import inspect
import re


class Analysis:
    def __init__(self, file):
        self.file = file
        self.hierarchy = self.get_class_hierarchy()
        # self.variables

    def get_class_hierarchy(self):
        hierarchy = {}
        for attr_name in dir(self.file):
            attr_instance = getattr(self.file, attr_name)
            if inspect.isclass(attr_instance):
                attr_parents = attr_instance.__bases__

                for parent in attr_parents:
                    class_parent = Class(parent.__name__, parent)
                    if parent in hierarchy:
                        hierarchy.get(class_parent).append(Class(attr_instance.__name__, attr_instance))
                    else:
                        hierarchy.update({class_parent: [Class(attr_instance.__name__, attr_instance)]})
        return hierarchy

    def get_children(self, class_name):
        children = []
        for item in self.hierarchy:
            if item.__name__ == class_name:
                print('item.__name__', item.__name__)
                children += self.hierarchy.get(item)
                for child in self.hierarchy.get(item):
                    deep_children_search = self.get_children(child.__name__, self.hierarchy)
                    if deep_children_search:
                        children += deep_children_search
        return children

    def get_parents(self, class_name):
        class_instance = getattr(self.file, class_name)
        mro = list(inspect.getmro(class_instance))[1:-1]
        return mro


class Class:
    def __init__(self, _name, _instance):
        self.name = _name
        self.instance = _instance

    def __str__(self):
        return 'Class %s' % (self.name)

    def __repr__(self):
        return 'Class %s' % (self.name)


class Method:
    def __init__(self, _name, _instance):
        self.name = _name
        self.instance = _instance
        self.source = inspect.getsource(_instance)

    def __str__(self):
        return 'Method %s %s' % (self.name, self.get_params())

    def __repr__(self):
        return 'Method %s %s' % (self.name, self.get_params())

    def get_params(self):
        return inspect.signature(self.instance)

    def get_variables(self):
        variables = self.instance.__code__.co_varnames
        # print('!'*10 , getattr(self.instance, ))
        return variables

    def find_calls(self):
        method_instance = self.instance
        print('method_instance', method_instance)
        method_source = inspect.getsource(method_instance)
        all_calls = re.findall(r'(\w+)\(', method_source)
        # print(self.instance.__code__.co_names)

        return set(all_calls[1:])


