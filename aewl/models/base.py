
import collections
import functools

from armaconfig.config import Config

from ..helpers import (Percentage, PixelGrid, PixelH, PixelW, SafeZoneH,
                       SafeZoneW, SafeZoneX, SafeZoneY, Operation, Factor)
from ..utils import inheritors
from ..defaults import ControlStyles, ControlTypes

Alias = collections.namedtuple('alias', ['key', 'value'])

def customizer(alias=None, optional=False, export=True, default=None):
    def wrapper(func):
        @functools.wraps(func)
        def call(self, k, *args, **kwargs):
            result = func(self, *args, **kwargs)
            
            if alias is not None:
                return Alias(alias, result)
            
            return Alias(k, result)

        call.export = export
        call.is_customizer = True
        call.optional = optional
        call.default = default

        return call
    return wrapper

def opt_customizer(default, *args, **kwargs):
    kwargs.setdefault('optional', True)
    kwargs['default'] = default

    return customizer(*args, **kwargs)

class Model:
    name = 'basic'
    fields = {
        'width': None,
        'height': None,
        'horizontal': 'start',
        'vertical': 'start',
        'id': -1,
        'style': 'no_rect',
        'type': 'static',
        'colorbackground': [0,0,0,0],
        'colortext': [1,1,1,1],
        'colorshadow': [0,0,0,0.5],
        'tooltipcolortext': [1,1,1,1],
        'tooltipcolorbox': [1,1,1,1],
        'tooltipcolorshade': [0,0,0,0.65],
        'shadow': 0,
        'text': '',
        'fixedwidth': 0,
        'font': 'PuristaLight',
        'linespacing': 1,
        'deletable': 0,
        'fade': 0,
        'access': 0,
        'default': 0,
        'blinkingperiod': 0,
        'moving': 0
    }

    def __new__(cls, typename, *args, **kwargs):
        for i in inheritors(cls, include_cls=True):
            if i.name == typename:
                inst = super().__new__(i)
                inst.__init__(*args, **kwargs)

                return inst

        raise Exception('Unknown base model {}'.format(typename))

    def __init__(self, skeleton, ctx=None):
        self.skeleton = skeleton
        self._ctx = ctx

    def set_ctx(self, ctx):
        self._ctx = ctx

    @property
    def ctx(self):
        if self._ctx is None:
            raise Exception('Context is none')
        
        return self._ctx

    def _make_control_operation(self, l, get_from):
        assert len(l) == 2

        make = []

        for i in l:
            if isinstance(i, list):
                make.append(self._make_control_operation(i, get_from))
            else:
                make.append(get_from.get(i.upper()))

        return Operation(make[0], make[1], op='+')

    @customizer(alias='style')
    def style(self, value):
        if isinstance(value, list):
            return self._make_control_operation(value, ControlStyles)

        return ControlStyles.get(value.upper())

    @customizer(alias='type')
    def type(self, value):
        if isinstance(value, list):
            return self._make_control_operation(value, ControlTypes)

        return ControlTypes.get(value.upper())

    def _make_pixel(self, len_name, val):
        if len_name == 'width':
            return PixelGrid.pixel_w(val)

        return PixelGrid.pixel_h(val)

    def _resolve_sizing(self, len_name, val):
        no_parent = self.ctx.parent.x_ctx is None

        if val is None:
            val = 0 if no_parent else Percentage(100)

        if isinstance(val, Percentage):
            if no_parent:
                raise Exception('no parent')

            return self.ctx.parent.x_ctx.processed(len_name) * (val / 100)
        elif len_name in ('width', 'height'):
            return self._make_pixel(len_name, val)
        else:
            raise Exception('BRO????')

    @customizer(alias='w')
    def width(self, value):
        """
        Width of the widget.
        Default is None, but is changed to 100% in _resolve_sizing if there exists a parent widget
        """
        return self._resolve_sizing('width', value)

    @customizer(alias='h')
    def height(self, value):
        """
        Height of the widget.
        Default is None, but is changed to 100% in _resolve_sizing if there exists a parent widget
        """
        return self._resolve_sizing('height', value)
    
    def _resolve_start(self, dir_):
        return 0

    def _resolve_directional(self, dir_, len_name, value):
        parent = self.ctx.parent.x_ctx

        if value == 'start':
            if parent is not None:
                # different for displays than for widgets
                return parent.model_method('_resolve_start', dir_)

            return 0
        elif value == 'center':
            return (
                parent.processed(len_name) / 2
                - self.ctx.processed(len_name) / 2
            )
        elif value == 'end':
            return (
                parent.processed(len_name)
                - self.ctx.processed(len_name)
            )

    @customizer(alias='x')
    def horizontal(self, value):
        return self._resolve_directional('horizontal', 'width', value)

    @customizer(alias='y')
    def vertical(self, value):
        return self._resolve_directional('vertical', 'height', value)

    @customizer(alias='idc')
    def id(self, value):
        return value

    @opt_customizer(False, export=False)
    def in_background(self, value):
        if not value:
            return None

        display = self.ctx.display_ctx or self.ctx.resource_ctx
        if display is None:
            raise Exception('in_background: no display')

        display.processed('body_background') # Make sure its been initialized before we add to it
        background = display.export['controlsbackground']
        background = background[display.model_method('bodyname_bg')]

        if 'controls' not in background:
            background['controls'] = {}

        background = background['controls']

        del self.ctx.obj['in_background']

        ctx = self.ctx.move(background)
        ctx.process_all()

        return None

    def _resolve_lean(self, dir_, len_name, towards, value):
        origin = self.ctx.processed(dir_)

        if value <= 0:
            return origin

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
    def left(self, value):
        """
        Lean towards left from the horizontal point
        """
        return self._resolve_lean('horizontal', 'width', 'start', value)

    @opt_customizer(Percentage(0), alias='x')
    def right(self, value):
        """
        Lean towards right from the horizontal point
        """
        return self._resolve_lean('horizontal', 'width', 'end', value)

    @opt_customizer(Percentage(0), alias='y')
    def top(self, value):
        """
        Lean towards top from the vertical point
        """
        return self._resolve_lean('vertical', 'height', 'start', value)

    @opt_customizer(Percentage(0), alias='y')
    def bottom(self, value):
        """
        Lean towards bottom from the vertical point
        """
        return self._resolve_lean('vertical', 'height', 'end', value)
