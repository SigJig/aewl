
import functools
import collections
from ..scope import Scope
from ..utils import inheritors
from ..helpers import (
    PixelH,
    PixelW,
    Percentage,
    SafeZoneW,
    SafeZoneH,
    SafeZoneX,
    SafeZoneY,
    PixelGrid
)

def customizer(default, alias=None):
    def wrapper(func):
        @functools.wraps(func)
        def call(self, k, *args, **kwargs):
            result = func(self, k, *args, **kwargs)
            
            if alias is not None:
                return {alias: result}
            
            return {k: result}

        call.is_customizer = True
        call.default = default

        return call
    return wrapper

class Widget(Scope):
    raw_name = 'basic_widget'

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
        self.processed = {}
        self.blacklist_props = []

        if not isinstance(self.parent_scope, Widget):
            self.parent_widget = None
        else:
            self.parent_widget = parent_scope

    def default(self, k, v):
        # TODO: Add warning
        self.processed[k] = {k: v}

    def get_processed(self, k):
        if k not in self.processed:
            self.process(k, self.properties.get(k, None))

        return next(iter(self.processed[k].values()))

    def process(self, k, v=None):
        try:
            meth = getattr(self, k)
            
            if not getattr(meth, 'is_customizer', False):
                raise AttributeError()
        except AttributeError:
            self.default(k, v)
        else:
            if v is None:
                v = meth.default

            result = meth(k, v)

            self.processed[k] = result

    def process_all(self):
        for attr in dir(self):
            method = getattr(self, attr)

            if getattr(method, 'is_customizer', False):
                try:
                    prop = self.get_property(attr)
                except KeyError:
                    prop = None

                self.process(attr, prop)

    def export(self):
        def _export(x):
            if isinstance(x, list):
                return [_export(y) for y in x]
            elif isinstance(x, dict):
                return {k: _export(v) for k, v in x.items()}
            elif hasattr(x, 'export'):
                return x.export()
            else:
                return x
        
        out = {}
        for val in self.processed.values():
            ek, ev = next(iter(val.items()))

            if ek in getattr(type(self), 'blacklist_props', []):
                continue

            out[ek] = _export(ev)
        
        return out

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
        kwargs.setdefault('parent_widget', self)
        return self.parent_scope.make_widget(*args, **kwargs)


    def _resolve_sizing(self, dir_, val):
        if isinstance(val, Percentage):
            if self.parent_widget is None:
                raise Exception('no parent')

            return self.parent_widget.get_processed(dir_) * (val / 100)
        elif dir_ == 'width':
            return PixelGrid.pixel_w(val)
        elif dir_ == 'height':
            return PixelGrid.pixel_h(val)
        else:
            raise Exception('BRO????')

    @customizer(Percentage(100), alias='w')
    def width(self, k, value):
        return self._resolve_sizing(k, value)

    @customizer(Percentage(100), alias='h')
    def height(self, k, value):
        return self._resolve_sizing(k, value)

    def _resolve_directional(self, dir_, len_name, value):
        if value == 'start':
            from . import display
            
            if isinstance(self.parent_widget, display.Display):
                return self.parent_widget.get_processed(dir_)
            
            return 0
        elif value == 'center':
            return (
                self.parent_widget.get_processed(len_name) / 2
                - self.get_processed(len_name) / 2
            )
        elif value == 'end':
            return (
                self.parent_widget.get_processed(len_name)
                - self.get_processed(len_name)
            )

    @customizer('start', alias='x')
    def horizontal(self, k, value):
        return self._resolve_directional(k, 'width', value)

    @customizer('start', alias='y')
    def vertical(self, k, value):
        return self._resolve_directional(k, 'height', value)

    @customizer(-1, alias='idc')
    def id(self, k, value):
        return value