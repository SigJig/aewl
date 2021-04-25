
from .base import Model

class Progress(Model):
    name = 'progress'
    fields = {
        **Model.fields,
        'type': 'progress',
        'style': 'left',
        'texture': '',
        'colorframe': [0,0,0,1],
        'colorbar': [0,0,0,1]
    }
