
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
        return {k: v.export(*args, **kwargs) for k, v in self.widgets.items()}

    def add_widget(self, name, *args, **kwargs):
        widget = self.make_widget(name, *args, **kwargs)
        self.widgets[name] = widget

        return widget

    def make_widget(self, name, inherits=[], is_display=False, parent_widget=None):
        inherits_wdg = []
        base_type = None

        for i in inherits:
            wdg = self.get_widget(i)

            if wdg is None:
                if base_type is not None:
                    raise Exception('Attempted inherit not found (%s)' % i)

                base_type = i

            inherits_wdg.append(wdg)

        type_ = Widget if not is_display else Display

        return type_.create(base_type, name, inherits_wdg, parent_widget or self)

    def get_widget(self, name):
        if name in self.widgets:
            return self.widgets.get(name)
        
        for li in self.links:
            found = li.get_widget(name)

            if found is not None:
                return found

        return None
