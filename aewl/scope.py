
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
