
from .base import Widget, customizer

class Group(Widget):
    raw_name = 'group'
    base_name = 'aewl_controlsgroupnoscroll'

    def add_children(self, body):
        for wdg in body:
            if isinstance(wdg, Widget):
                wdg.set_parent_widget(self)

        self.add_property('children', body)

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
    base_name = 'aewl_progress'