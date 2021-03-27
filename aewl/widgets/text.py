
from .base import Widget, customizer
from ..helpers import Percentage, PixelGrid

class Text(Widget):
    raw_name = 'text'
    base_name = 'aewl_text'

    def _resolve_size(self, k, val):
        if isinstance(val, Percentage):
            return self.get_processed('height') * (val / 100)
        else:
            return PixelGrid.pixel_h(val)

    @customizer(Percentage(100), alias='sizeEx')
    def size(self, k, val):
        return self._resolve_size(k, val)

class StructuredText(Text):
    raw_name = 'structured_text'
    base_name = 'aewl_structuredtext'

    @customizer(Percentage(100), alias='size')
    def size(self, k, val):
        # Just changes alias to size instead of sizeEx
        return self._resolve_size(k, val)
