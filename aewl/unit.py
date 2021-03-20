
class Scope:
    def __init__(self, name, parent=None):
        self.name = name
        self.variables = {}
        self.parent = parent

    def __str__(self):
        return self.name

    def add_variable(self, key, value):
        self.variables[key] = value

    def get_variable(self, key):
        try:
            return self.variables[key]
        except KeyError:
            if self.parent is not None:
                return self.parent.get_variable(key)
            
            raise

class Unit(Scope):
    def __init__(self, name):
        self.links = []
        self.widgets = {}

        super().__init__(name)

    def export(self):
        return {str(self): {k: v.export() for k, v in self.widgets.items()}}

    def add_widget(self, name, *args, **kwargs):
        widget = self.make_widget(name, *args, **kwargs)
        self.widgets[name] = widget

        return widget

    def make_widget(self, name, inherits=[], is_display=False):
        inherits_wdg = []

        for i in inherits:
            wdg = self.get_widget(i)

            if wdg is None:
                raise Exception('Attempted inherit not found (%s)' % i)

            inherits_wdg.append(wdg)

        type_ = Widget if not is_display else Display

        return type_(name, inherits_wdg, self)

    def get_widget(self, name):
        if name in self.widgets:
            return self.widgets.get(name)
        
        for li in self.links:
            found = li.get_widget(name)

            if found is not None:
                return found

        return None

class Widget(Scope):
    def __init__(self, name, inherits=[], parent=None):
        self.name = name
        self.inherits = inherits
        self.properties = {}

        super().__init__(name=name, parent=parent)

    def export(self):
        def _export(x):
            if isinstance(x, list):
                return [_export(y) for y in x]
            elif hasattr(x, 'export'):
                return x.export()
            else:
                return x
        
        return {k: _export(v) for k, v in self.properties.items()}

    def add_property(self, key, value):
        self.properties[key] = value

    def get_property(self, key):
        try:
            return self.properties[key]
        except KeyError:
            if isinstance(self.parent, Widget):
                return self.parent.get_property(key)

            raise

    def make_widget(self, *args, **kwargs):
        return self.parent.make_widget(*args, **kwargs)

class Display(Widget):
    pass