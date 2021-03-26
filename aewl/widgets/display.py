
from .base import Widget, customizer
from .group import Group
from ..helpers import (
    Percentage,
    SafeZoneW,
    SafeZoneH,
    SafeZoneX,
    SafeZoneY
)

BODYNAME = 'aewl_body'
BODYNAME_BACKGROUND = 'aewl_body_background'

class Display(Widget):
    # Skip x y w h, as it does nothing on a display
    # Might change it later so that only props in
    # a whitelist array are passed instead.
    blacklist_props = ['x', 'y', 'w', 'h']
    raw_name = None
    base_name = None

    def _resolve_sizing(self, dir_, val):
        if isinstance(val, Percentage):
            val = val / 100

        if dir_ == 'width':
            return SafeZoneW(val)
        elif dir_ == 'height':
            return SafeZoneH(val)
        else:
            raise Exception('BRO????')

    def _resolve_directional(self, dir_, len_name, value):
        sz_type, sz_unit = (
            (SafeZoneX(), SafeZoneW(1)) if len_name == 'width' else (SafeZoneY(), SafeZoneH(1))
        )

        if value == 'start':
            return sz_type
        elif value == 'center':
            return (
                (sz_type + sz_unit) / 2
                - self.get_processed(len_name) / 2
            )
        elif value == 'end':
            return (
                (sz_type) + sz_unit
                - self.get_processed(len_name)
            )

    def _layer_group(self, name, body):
        """
        Inserts a group between the displays and the widgets
        defined in the body.
        This is so that position can be calculated relative to the display
        """
        group = Group(name, [], self)
        group.add_children(body)
        group.process_all()

        return group

    @customizer([], alias='controls')
    def body(self, k, body):
        return {
            BODYNAME: self._layer_group(BODYNAME, body)}

    @customizer([], alias='controlsBackground')
    def body_background(self, k, body):
        return {
            BODYNAME_BACKGROUND: self._layer_group(BODYNAME_BACKGROUND, body)}

    @customizer(-1, alias='idd')
    def id(self, k, value):
        return value