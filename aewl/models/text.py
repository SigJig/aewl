
from .base import customizer, Model
from ..helpers import Percentage, PixelGrid

class Text(Model):
    name = 'text'
    fields = {
        **Model.fields,
        'style': ['left', 'multi'],
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
    name = 'structured_text'
    fields = {
        **Model.fields,
        'type': 'structured_text',
        'style': 'left',
        'attributes': {
            'color': '#ffffff',
            'colorlink': '#D09B43',
            'align': 'left'
        }
    }

    @customizer(alias='size')
    def size(self, val):
        # Just changes alias to size instead of sizeEx
        return self._resolve_sizeEx(val)
