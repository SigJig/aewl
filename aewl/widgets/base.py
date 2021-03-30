
import collections
import functools

from armaconfig.config import Config

from ..helpers import (Percentage, PixelGrid, PixelH, PixelW, SafeZoneH,
                       SafeZoneW, SafeZoneX, SafeZoneY, Operation)
from ..scope import Scope, ContainerScope
from ..utils import inheritors
from ..defaults import ControlStyles, ControlTypes

Alias = collections.namedtuple('alias', ['key', 'value'])

def customizer(default, alias=None, optional=False):
    def wrapper(func):
        @functools.wraps(func)
        def call(self, k, *args, **kwargs):
            result = func(self, k, *args, **kwargs)
            
            if alias is not None:
                return Alias(alias, result)
            
            return Alias(k, result)

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
        inherits = kwargs.get('inherits', [])
        if type_ is None:
            cls_type = cls

            try:
                last_inherit = next(reversed(inherits))
            except StopIteration:
                pass
            else:
                cls_type = type(last_inherit)
            
            return cls_type(*args, **kwargs)

        for t in inheritors(cls):
            if getattr(t, 'raw_name', None) == type_:
                return t(*args, **kwargs)

        raise Exception('widget type {} not found'.format(type_))

    def __init__(self, name, inherits=[], parent_scope=None):
        super().__init__(name=name, parent_scope=parent_scope)

        self.inherits = inherits
        self.output = {} # Output contains ready-to-be exported data
        self.properties = {} # Properties raw after parsing
        self.processed = {} # Cache for processed properties
        self.blacklist_props = []

        if not isinstance(self.parent_scope, Widget):
            par = self.parent_scope
            while par is not None:
                if not isinstance(par, Widget):
                    par = par.parent_scope
                else:
                    break
  
            self.parent_widget = par
        else:
            self.set_parent_widget(parent_scope)

    def set_parent_widget(self, wdg):
        self.parent_widget = wdg

    def _default(self, k, v):
        # TODO: Add warning
        self.processed[k] = Alias(k, v)
        self.output[k] = v

    def get_raw(self, k):
        return self.output[k]

    def get_processed(self, k):
        return self.process(k)

    def process(self, k):
        if k in self.processed:
            return self.processed[k].value

        try:
            value = self.get_property(k)
        except KeyError:
            value = None

        try:
            meth = getattr(self, k)
            
            if not getattr(meth, 'is_customizer', False):
                raise AttributeError()
        except AttributeError:
            return self._default(k, value)
        else:
            if value is not None or not meth.optional:
                if value is None:
                    value = meth.default

                result = meth(k, value)

                self.processed[k] = result
                self.output[result.key] = result.value

                return result.value

            return value

    def process_all(self):
        props = list(self.properties.keys())
        for attr in props + (
                [x
                for x in dir(self)
                if x not in props and getattr(getattr(self, x, None), 'is_customizer', False)]
                ):
            self.process(attr)

    def export(self, parent=None):
        if self.inherits:
            inherits_name = next(iter(self.inherits)).name
        else:
            inherits_name = getattr(self, 'base_name', getattr(self, 'raw_name', None))

        conf = Config(self.name,
            inherits_name,
            parent
        )

        def _export(x, n=None, cfg=None):
            cfg = cfg if cfg is not None else conf
            if isinstance(x, ContainerScope):
                return _export(x.export(), n, cfg)
            elif isinstance(x, list):
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

        for k, v in self.output.items():
            if k in getattr(type(self), 'blacklist_props', []):
                continue

            conf.add(_export(v, k), k)
        
        return conf

    def get(self, key):
        try:
            return self.get_property(key)
        except KeyError:
            return super().get(key)

    def add_property(self, key, value):
        self.properties[key] = value

    def get_property(self, key):
        try:
            return self.properties[key]
        except KeyError:
            for i in self.inherits:
                try:
                    if isinstance(i, Widget):
                        return i.get_property(key)
                except KeyError:
                    pass

            raise

    def make_widget(self, *args, **kwargs):
        kwargs.setdefault('parent_widget', self)

        return self.parent_scope.make_widget(*args, **kwargs)

    def _make_pixel(self, len_name, val):
        if len_name == 'width':
            return PixelGrid.pixel_w(val)

        return PixelGrid.pixel_h(val)

    def _resolve_sizing(self, len_name, val):
        if val is None:
            val = 0 if self.parent_widget is None else Percentage(100)

        if isinstance(val, Percentage):
            if self.parent_widget is None:
                raise Exception('no parent')

            return self.parent_widget.get_processed(len_name) * (val / 100)
        elif len_name in ('width', 'height'):
            return self._make_pixel(len_name, val)
        else:
            raise Exception('BRO????')

    @customizer(None, alias='w')
    def width(self, k, value):
        """
        Width of the widget.
        Default is None, but is changed to 100% in _resolve_sizing if there exists a parent widget
        """
        return self._resolve_sizing(k, value)

    @customizer(None, alias='h')
    def height(self, k, value):
        """
        Height of the widget.
        Default is None, but is changed to 100% in _resolve_sizing if there exists a parent widget
        """
        return self._resolve_sizing(k, value)
    
    def _resolve_start(self, dir_):
        return 0

    def _resolve_directional(self, dir_, len_name, value):
        if value == 'start':
            if self.parent_widget is not None:
                # different for displays than for widgets
                return self.parent_widget._resolve_start(dir_)

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

    def _resolve_lean(self, dir_, len_name, towards, value):
        origin = self.get_processed(dir_)

        if isinstance(value, Percentage):
            towards_point = self._resolve_directional(dir_, len_name, towards)

            if towards == 'start':
                return ((origin - towards_point) * ((100 - value) / 100)) + towards_point
            
            return ((towards_point - origin) * (value / 100)) + origin
        else:
            if towards == 'start':
                return origin - self._make_pixel(len_name, value)
            
            return origin + self._make_pixel(len_name, value)

    @opt_customizer(Percentage(0), alias='x')
    def left(self, k, value):
        """
        Lean towards left from the horizontal point
        """
        return self._resolve_lean('horizontal', 'width', 'start', value)

    @opt_customizer(Percentage(0), alias='x')
    def right(self, k, value):
        """
        Lean towards right from the horizontal point
        """
        return self._resolve_lean('horizontal', 'width', 'end', value)

    @opt_customizer(Percentage(0), alias='y')
    def top(self, k, value):
        """
        Lean towards top from the vertical point
        """
        return self._resolve_lean('vertical', 'height', 'start', value)

    @opt_customizer(Percentage(0), alias='y')
    def bottom(self, k, value):
        """
        Lean towards bottom from the vertical point
        """
        return self._resolve_lean('vertical', 'height', 'end', value)

    def _make_control_operation(self, l, get_from):
        assert len(l) == 2

        make = []

        for i in l:
            if isinstance(i, list):
                make.append(self._make_control_operation(i, get_from))
            else:
                make.append(get_from.get(i.upper()))

        return Operation(make[0], make[1], op='+')

    @opt_customizer('left', alias='style')
    def style(self, k, value):
        if isinstance(value, list):
            return self._make_control_operation(value, ControlStyles)

        return ControlStyles.get(value.upper())

    @opt_customizer('static', alias='type')
    def type(self, k, value):
        if isinstance(value, list):
            return self._make_control_operation(value, ControlTypes)

        return ControlTypes.get(value.upper())
