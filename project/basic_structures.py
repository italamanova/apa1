import inspect


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

    def __str__(self):
        return 'Class %s' % (self.name)

    def __repr__(self):
        return 'Class %s' % (self.name)


class Method:
    def __init__(self, _name, _params):
        self.name = _name
        self.params = _params

    def __str__(self):
        return 'Method %s %s' % (self.name, self.params)

    def __repr__(self):
        return 'Method %s %s' % (self.name, self.params)
