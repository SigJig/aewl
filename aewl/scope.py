
class Scope:
    def __init__(self, name, parent_scope=None):
        self.name = name
        self.variables = {}
        self.parent_scope = parent_scope

        # if the current parsing happens within an array, we need to keep
        # track of previous items in the array.
        # this is for things like the 'children' property, which is an
        # array of widgets that may depend on each other through inheritance
        self.temp_array = []

    def __str__(self):
        return self.name

    def add_variable(self, key, value):
        self.variables[key] = value

    def get_variable(self, key):
        try:
            return self.variables[key]
        except KeyError:
            if self.parent_scope is not None:
                return self.parent_scope.get_variable(key)
            
            raise
