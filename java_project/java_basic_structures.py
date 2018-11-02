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
        print('class_name', self.class_name)
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
