
from collections import OrderedDict

class Scope:
    def __init__(self, name, parent_scope=None):
        self.name = name
        self.macros = {}
        self.parent_scope = parent_scope

    def __str__(self):
        return self.name

    def add_macro(self, key, value):
        self.macros[key] = value

    def get(self, key):
        try:
            return self.macros[key]
        except KeyError:
            if self.parent_scope is not None:
                return self.parent_scope.get(key)

            raise

class ContainerScope(Scope):
    def __init__(self, container, parent_scope):
        self.container = container

        super().__init__(None, parent_scope)

    def export(self):
        return self.container

    def __getattr__(self, attr, *args, **kwargs):
        if attr in dir(self.parent_scope):
            return getattr(self.parent_scope, attr, *args, **kwargs)

        return getattr(self.container, attr, *args, **kwargs)

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, repr(self.container))

    def __str__(self):
        return str(self.container)

    def __getitem__(self, key):
        return self.container[key]

    def __setitem__(self, key, value):
        self.container[key] = value

    def __iter__(self):
        return iter(self.container)

class ListScope(ContainerScope, list):
    def get(self, key):
        for x in self.container:
            if getattr(x, 'name', None) == key:
                return x

        return super().get(key)

    def append(self, item):
        self.container.append(item)

class DictScope(ContainerScope, dict):
    def __init__(self, container, *args, **kwargs):
        if not isinstance(container, OrderedDict):
            container = OrderedDict(container)

        super().__init__(container, *args, **kwargs)

    def get(self, key):
        if key in self.container:
            return self.container.get(key)

        return super().get(key)