
from .base import customizer, Model
from ..helpers import Percentage, PixelGrid

class Text(Model):
    name = 'text'
    fields = {
        **Model.fields,
        'style': ['left', 'multi', 'no_rect']
    }

class StructuredText(Text):
    name = 'structured_text'
    fields = {
        **Model.fields,
        'type': 'structured_text',
        'style': ['left', 'no_rect'],
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

class Input(Model):
    name = 'input'
    fields = {
        **Model.fields,
        'type': 'edit',
        'style': ['left', 'frame'],
        'canModify': True,
        'autocomplete': ''
    }