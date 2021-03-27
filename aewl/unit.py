
from armaconfig.config import Config
from .scope import Scope
from .widgets import Widget, Display

class Unit(Scope):
    def __init__(self, name):
        self.links = []
        self.widgets = {}

        super().__init__(name)

    def process_all(self):
        for v in self.widgets.values():
            v.process_all()

    def export(self, *args, **kwargs):
        conf = Config(self.name, parent=kwargs.get('parent', None))
        kwargs['parent'] = conf

        for v in self.widgets.values():
            conf.add(v.export(*args, **kwargs))

        return conf

    def add_widget(self, name, *args, **kwargs):
        widget = self.make_widget(name, *args, **kwargs)
        self.widgets[name] = widget

        return widget

    def make_widget(self, name, inherits=[], type_=Widget, parent_widget=None, temp_array=[]):
        inherits_wdg = []
        base_type = None
        temp_dict = {}

        for w in temp_array:
            if isinstance(w, Widget):
                temp_dict[w.name] = w

        for i in inherits:
            if i in temp_dict:
                wdg = temp_dict[i]
            else:
                wdg = self.get_widget(i)

            if wdg is None:
                if base_type is not None:
                    raise Exception('Attempted inherit not found (%s)' % i)

                base_type = i
            else:
                inherits_wdg.append(wdg)

        return type_.create(base_type, name, inherits=inherits_wdg, parent_scope=parent_widget or self)

    def get_widget(self, name):
        if name in self.widgets:
            return self.widgets.get(name)
        
        for li in self.links:
            found = li.get_widget(name)

            if found is not None:
                return found

        return None
