
import functools
import collections

from armaconfig.config import Config

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

def make_alias(alias, v):
    return {alias: v}

def customizer(default, alias=None, optional=False):
    def wrapper(func):
        @functools.wraps(func)
        def call(self, k, *args, **kwargs):
            result = func(self, k, *args, **kwargs)

            if result is None:
                return None
            
            if alias is not None:
                return make_alias(alias, result)
            
            return {k: result}

        call.is_customizer = True
        call.default = default
        call.optional = optional

        return call
    return wrapper

def opt_customizer(*args, **kwargs):
    kwargs.setdefault('optional', True)
    return customizer(*args, **kwargs)

class Widget(Scope):
    raw_name = 'basic'
    base_name = 'aewl_basics'
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
            self.set_parent_widget(parent_scope)

    def set_parent_widget(self, wdg):
        self.parent_widget = wdg

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
            if v is not None or not meth.optional:
                if v is None:
                    v = meth.default

                result = meth(k, v)

                if result is not None:
                    self.processed[k] = result

    def get_customizers(self):
        return set({x for x in dir(self)
                        if getattr(getattr(self, x, None), 'is_customizer', False)})

    def process_all(self):
        for attr in self.get_customizers().union(self.properties.keys()):
            try:
                prop = self.get_property(attr)
            except KeyError:
                prop = None

            self.process(attr, prop)

    def export(self, parent=None):
        conf = Config(self.name,
            getattr(self, 'base_name', getattr(self, 'raw_name', None)),
            parent
        )

        def _export(x, n=None, cfg=None):
            cfg = cfg if cfg is not None else conf
            if isinstance(x, list):
                return [_export(y) for y in x]
            elif isinstance(x, dict):
                cur_cfg = Config(n, parent=cfg)

                for k, v in x.items():
                    cur_cfg.add(_export(v, k, cur_cfg), k)

                return cur_cfg
            elif hasattr(x, 'export'):
                if isinstance(x, Widget):
                    return x.export(cfg)

                return x.export()
            else:
                return x

        for val in self.processed.values():
            ek, ev = next(iter(val.items()))

            if ek in getattr(type(self), 'blacklist_props', []):
                continue

            conf.add(_export(ev, ek), ek)
        
        return conf

    def add_property(self, key, value):
        self.properties[key] = value

    def get_property(self, key):
        try:
            return self.properties[key]
        except KeyError:
            for i in self.inherits:
                try:
                    if isinstance(i, Widget):
                        return self.parent_scope.get_property(key)
                except KeyError:
                    pass

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

    @opt_customizer(Percentage(0), alias='x')
    def left(self, k, value):
        horiz = self.get_processed('horizontal')
        start = self._resolve_directional('horizontal', 'width', 'start')

        print(horiz, start, value)

        self.processed['horizontal'] = make_alias('x', ((horiz - start) * ((100 - value) / 100)) + start)