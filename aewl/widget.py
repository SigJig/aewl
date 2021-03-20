
class Widget:
    def __init__(self, name, inherits=[], unit=None):
        self.name = name
        self.inherits = inherits
        self.properties = {}
        self.unit = unit

    def export(self): pass

    def add_property(self): pass
