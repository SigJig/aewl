
from .base import Model, customizer

class Group(Model):
    name = 'group'
    fields = {
        **Model.fields,
        'vscrollbar': {
            'width': 0
        },
        'hscrollbar': {
            'height': 0
        },
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

class ScrollableH(Group):
    name = 'scrollableH'
    fields = {
        **Group.fields,
        'hscrollbar': {

        }
    }

class ScrollableW(Group):
    name = 'scrollableW'
    fields = {
        **Group.fields,
        'vscrollbar': {
            
        }
    }

class ScrollableHW(Group):
    name = 'scrollable'
    fields = {
        **Group.fields,
        'hscrollbar': {
            
        },
        'vscrollbar': {

        }
    }
