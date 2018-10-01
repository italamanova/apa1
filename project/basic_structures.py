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
