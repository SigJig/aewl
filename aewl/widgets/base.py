
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
        for k, v in self.properties.items():
            self.process(k, v)

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
            k, v = next(iter(val.items()))

            out[k] = _export(v)
        
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

    def _resolve_directional(self, dir_, value):
        if value == 'start':
            return 0
        elif value == 'center':
            return (
                self.parent_widget.get_processed(dir_) / 2
                - self.get_processed(dir_) / 2
            )
        elif value == 'end':
            return (
                self.parent_widget.get_processed(dir_)
                - self.get_processed(dir_)
            )

    @customizer('start', alias='x')
    def horizontal(self, k, value):
        return self._resolve_directional('width', value)

    @customizer('start', alias='y')
    def vertical(self, k, value):
        return self._resolve_directional('height', value)
