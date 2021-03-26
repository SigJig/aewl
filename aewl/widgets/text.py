
from .base import Widget, customizer
from ..helpers import Percentage, PixelGrid

class Text(Widget):
    raw_name = 'text'
    base_name = 'aewl_text'

    @customizer(Percentage(100), alias='sizeEx')
    def size(self, k, val):
        if isinstance(val, Percentage):
            return self.get_processed('height') * (val / 100)
        else:
            return PixelGrid.pixel_h(val)
