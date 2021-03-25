
from .base import Widget, customizer

class Group(Widget):
    raw_name = 'group'

    @customizer([], alias='controls')
    def children(self, k, body):
        if not isinstance(body, list):
            raise TypeError('Expected list, got {}'.format(type(body)))

        results = {}

        for x in body:
            x.process_all()
            results[x.name] = x

        return results

class Progress(Widget):
    raw_name = 'progress'