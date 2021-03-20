
from collections import defaultdict
from scope import Scope

class _Meta(type):
    def __new__(cls, name, bases, attrs):
        pass

class Widget(Scope):
    class __metaclass__(type):
        __inheritors__ = defaultdict(list)

        def __new__(meta, name, bases, dct):
            klass = type.__new__(meta, name, bases, dct)
            for base in klass.mro()[1:-1]:
                meta.__inheritors__[base].append(klass)
            return klass

    def __init__(self, name, inherits=[], parent=None):
        self.name = name
        self.inherits = inherits
        self.properties = {}

        super().__init__(name=name, parent=parent)

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
            if isinstance(self.parent, Widget):
                return self.parent.get_property(key)

            raise

    def make_widget(self, *args, **kwargs):
        return self.parent.make_widget(*args, **kwargs)

class Display(Widget):
    pass