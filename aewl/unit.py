
from armaconfig.config import Config
from .types import Widget, Display

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

class Unit:
    def __init__(self, name):
        self.name = name
        self.links = []
        self.widgets = {}
        self.macros = {}

    def add_link(self, *args, **kwargs):
        kwargs['root'] = self

        self.links.append(Link(*args, **kwargs))

    def add_widget(self, name, *args, **kwargs):
        widget = self.make_widget(name, *args, **kwargs)
        self.widgets[name] = widget

        return widget

    def make_widget(self, name, inherits=None, type_=Widget):
        return type_(name, inherits=inherits)

    def __getitem__(self, key):
        if key in self.widgets:
            return self.widgets[key]
        else:
            for link in self.links:
                try:
                    return link.get(key)
                except KeyError:
                    pass

            raise KeyError(key)
