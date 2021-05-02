
from .text import Text

class Picture(Text):
    name = 'picture'
    fields = {
        **Text.fields,
        'style': ['picture']
    }
