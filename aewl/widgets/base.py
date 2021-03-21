
from collections import defaultdict
from ..scope import Scope
from ..utils import inheritors
from ..helpers import (
    PixelH,
    PixelW,
    Percentage
)

def customizer(func):
    func.is_customizer = True

    return func

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
        self.output = {}

        if not isinstance(self.parent_scope, Widget):
            self.parent_widget = None
        else:
            self.parent_widget = parent_scope

    def default(self, k, v):
        self.output[k] = v

    def process(self, k, v):
        meth = getattr(self, k, self.default)

        if not getattr(meth, 'is_customizer', False):
            meth = self.default
        
        response = meth(k, v)

        if response is not None:
            self.output[k] = response

    def process_all(self):
        for k, v in self.properties.items():
            self.process(k, v)

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


    def _resolve_sizing(self, dir_, val):
        if isinstance(val, Percentage):
            if self.parent_widget is None:
                raise Exception('no parent')

            raise Exception('calm down cunt i havent implemented this yet')
            #return getattr(self.parent_widget, dir_)() * (val / 100)
        elif dir_ == 'width':
            return PixelW(val)
        elif dir_ == 'height':
            return PixelH(val)
        else:
            raise Exception('BRO????')

    @customizer
    def width(self, k, value):
        return self._resolve_sizing(k, value)

    @customizer
    def height(self, k, value):
        return self._resolve_sizing(k, value)

    @customizer
    def size(self, k, value):
        self.output['width'] = self.width('width', value)
        self.output['height'] = self.height('height', value)

class Display(Widget): pass
