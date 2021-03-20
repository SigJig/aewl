
class Scope:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

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
        self.name = name

        self.links = []
        self.widgets = {}

        super().__init__()

    def add_widget(self, name, *args, **kwargs):
        widget = self.make_widget(name, *args, **kwargs)
        self.widgets[name] = widget

        return widget

    def make_widget(self, name, inherits_name=None, is_display=False):
        if inherits_name is None:
            inherits = self.get_widget(inherits_name)

            if inherits is None:
                raise Exception('Attempted inherit not found (%s)' % inherits_name)
        else:
            inherits = None

        type_ = Widget if not is_display else Display

        return type_(name, inherits, self)

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

        super().__init__(parent=parent)

    def export(self): pass

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