
from collections import defaultdict
from scope import Scope
from utils import inheritors

class Widget(Scope):
    @classmethod
    def create(cls, type_, *args, **kwargs):
        if type_ is None:
            return cls(*args, **kwargs)

        for t in inheritors(cls):
            if getattr(t, 'raw_name', None) == type_:
                return t(*args, **kwargs)

        raise Exception('widget type {} not found'.format(type_))

    def __init__(self, name, inherits=[], parent_scope=None):
        super().__init__(name=name, parent_scope=parent_scope)

        self.inherits = inherits
        self.properties = {}


    def export(self):
        def _export(x):
            if isinstance(x, list):
                return [_export(y) for y in x]
            elif hasattr(x, 'export'):
                return x.export()
            else:
                return x
        
        return {k: _export(v) for k, v in self.properties.items()}

    def add_property(self, key, value):
        self.properties[key] = value

    def get_property(self, key):
        try:
            return self.properties[key]
        except KeyError:
            if isinstance(self.parent_scope, Widget):
                return self.parent_scope.get_property(key)

            raise

    def make_widget(self, *args, **kwargs):
        return self.parent_scope.make_widget(*args, **kwargs)

class Display(Widget):
    pass