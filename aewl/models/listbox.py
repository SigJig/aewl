
from .base import Model, customizer
from helpers import PixelH

class Listbox(Model):
    name = 'listbox'
    fields = {
        **Model.fields,
        'style': ['multi'],
        'type': 'listbox',
        'maxHistoryDelay': 1,
        'listscrollbar': {
            'color': [1, 1, 1, 1],
            'autoScrollEnabled': True
        },
        'period': 1,
        'rowHeight': PixelH(1)
    }