
from .base import Widget, customizer

class Group(Widget):
    raw_name = 'group_widget'

    @customizer
    def children(self, k, body):
        if not isinstance(body, list):
            raise TypeError('Expected list, got {}'.format(type(body)))

        if 'controls' not in self.output:
            self.output['controls'] = {}

        for x in body:
            x.process_all()
            self.output['controls'][x.name] = x

class Text(Widget):
    raw_name = 'text_widget'

class Progress(Widget):
    raw_name = 'progress_widget'