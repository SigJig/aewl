
from .base import customizer, Model
from .group import Group
from ..helpers import (
    Percentage,
    SafeZoneW,
    SafeZoneH,
    SafeZoneX,
    SafeZoneY
)
from ..types import Widget

BODYNAME = 'aewl_body'
BODYNAME_BACKGROUND = 'aewl_body_background'

class DisplayModel(Model):
    name = None
    fields = {
        'width': None,
        'height': None,
        'horizontal': 'start',
        'vertical': 'start',
        'id': -1,
        'body': [],
        'body_background': [],
        'enablesimulation': True,
        'access': 0
    }

    def _resolve_sizing(self, dir_, val):
        if val is None:
            val = Percentage(100)

        if isinstance(val, Percentage):
            val = val / 100

            if dir_ == 'width':
                return SafeZoneW(val)
            elif dir_ == 'height':
                return SafeZoneH(val)
            else:
                raise Exception('BRO????')
        else:
            return super()._resolve_sizing(dir_, val)

    def _resolve_start(self, dir_):
        return self.ctx.processed(dir_)

    def _resolve_directional(self, dir_, len_name, value):
        sz_type, sz_unit = (
            (SafeZoneX(), SafeZoneW(1)) if len_name == 'width' else (SafeZoneY(), SafeZoneH(1))
        )

        if value == 'start':
            return sz_type
        elif value == 'center':
            return (
                (sz_type + sz_unit) / 2
                - self.ctx.processed(len_name) / 2
            )
        elif value == 'end':
            return (
                (sz_type) + sz_unit
                - self.ctx.processed(len_name)
            )

    def _layer_group(self, name, body):
        """
        Inserts a group between the displays and the widgets
        defined in the body.
        This is so that position can be calculated relative to the display
        """
        if not len(body):
            return {}

        wdg = Widget(name, inherits=['group'])
        wdg['children'] = body

        ctx = self.ctx.add_child(wdg)
        ctx.process_all()

        return ctx.export

    @customizer(alias='controls')
    def body(self, body):
        return {
            BODYNAME: self._layer_group(BODYNAME, body)}

    @customizer(alias='controlsbackground')
    def body_background(self, body):
        return {
            BODYNAME_BACKGROUND: self._layer_group(BODYNAME_BACKGROUND, body)}

    @customizer(alias='idd')
    def id(self, value):
        return value

    @customizer(export=False)
    def width(self, value):
        return self._resolve_sizing('width', value)

    @customizer(export=False)
    def height(self, value):
        return self._resolve_sizing('height', value)

    @customizer(export=False)
    def horizontal(self, value):
        return self._resolve_directional('horizontal', 'width', value)

    @customizer(export=False)
    def vertical(self, value):
        return self._resolve_directional('vertical', 'height', value)
