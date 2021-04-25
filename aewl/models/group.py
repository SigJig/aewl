
from .base import Model, customizer

class Group(Model):
    name = 'group'
    fields = {
        **Model.fields,
        'vscrollbar': {
            'umm': 2
        },
        'hscrollbar': {},
        'type': 'controls_group',
        'children': []
    }

    @customizer(alias='controls')
    def children(self, body):
        if not isinstance(body, list):
            raise TypeError('Expected list, got {}'.format(type(body)))

        r = {}

        for x in body:
            ctx = self.ctx.add_child(x)
            ctx.process_all()

            r[x.name] = ctx.export

        return r
