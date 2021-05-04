
from .base import customizer, Model
from ..helpers import Percentage, PixelGrid

class Text(Model):
    name = 'text'
    fields = {
        **Model.fields,
        'style': ['left', 'multi']
    }

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
