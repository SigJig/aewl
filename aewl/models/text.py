
from .base import customizer, Model
from ..helpers import Percentage, PixelGrid

class Text(Model):
    raw_name = 'text'
    base_name = 'aewl_text'
    fields = {
        **Model.fields,
        'size': Percentage(100)
    }

    def _resolve_sizeEx(self, val):
        if isinstance(val, Percentage):
            return self.ctx.processed('height') * (val / 100)
        else:
            return PixelGrid.pixel_h(val)

    @customizer(alias='sizeEx')
    def size(self, val):
        return self._resolve_sizeEx(val)

class StructuredText(Text):
    raw_name = 'structured_text'
    base_name = 'aewl_structuredtext'

    @customizer(alias='size')
    def size(self, val):
        # Just changes alias to size instead of sizeEx
        return self._resolve_sizeEx(val)
