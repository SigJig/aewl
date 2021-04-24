
from .base import Model, customizer

class Group(Model):
    raw_name = 'group'
    base_name = 'aewl_controlsgroupnoscroll'
    fields = {
        **Model.fields,
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

            r[x.name] = x

        return r

class Progress(Model):
    raw_name = 'progress'
    base_name = 'aewl_progress'
