
from widget import Widget

class Unit:
    def __init__(self, name):
        self.name = name

        self.links = []
        self.widgets = {}
        self.variables = {}

    def add_widget(self, name, inherits_name=None):
        if inherits_name is not None:
            inherits = self.get_widget(inherits_name)

            if inherits is None:
                raise Exception('Attempted inherit not found (%s)' % inherits_name)
        else:
            inherits = None

        return Widget(name, inherits, self)

    def get_widget(self, name):
        if name in self.widgets:
            return self.widgets.get(name)
        
        for li in self.links:
            found = li.get_widget(name)

            if found is not None:
                return found

        return None
