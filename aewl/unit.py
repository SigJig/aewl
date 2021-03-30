
from armaconfig.config import Config
from .scope import Scope
from .widgets import Widget, Display

class Link:
    def __init__(self, unit, root, partials=[]):
        self.unit = unit
        self.root = root
        self.partials = partials

    def _verify_partials(self, key):
        if self.partials and key not in self.partials:
            raise KeyError(key)

    def get(self, key):
        self._verify_partials(key)

        return self.unit.get(key)

    def __getattr__(self, *args, **kwargs):
        return getattr(self.unit, *args, **kwargs)

class Unit(Scope):
    def __init__(self, name):
        self.links = []
        self.widgets = {}

        super().__init__(name)

    def add_link(self, unit):
        self.links.append(Link(unit, self))

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

    def make_widget(self, name, inherits=[], type_=Widget, parent_widget=None):
        inherits_wdg = []
        base_type = None
        for i in inherits:
            try:
                inherits_wdg.append(parent_widget.get(i))
            except KeyError:
                if base_type is not None:
                    raise Exception('Attempted inherit not found (%s)' % i)

                base_type = i

        return type_.create(base_type, name, inherits=inherits_wdg,
                parent_scope=parent_widget if parent_widget is not None else self)

    def get(self, key):
        if key in self.macros:
            return self.macros[key]
        elif key in self.widgets:
            return self.widgets[key]
        else:
            for link in self.links:
                try:
                    return link.get(key)
                except KeyError:
                    pass

            raise KeyError(key)

    def get_widget(self, name):
        wdg = self.get(name)

        if not isinstance(wdg, Widget):
            raise TypeError(
                'Expected {}, got {}'.format(Widget.__name__, type(wdg).__name__))

        return wdg