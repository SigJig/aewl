
class PixelH(float):
    def __str__(self):
        return '{}pixelH'.format(float(self))

    def __repr__(self):
        return str(self)

    def export(self):
        return '({} * pixelH * pixelGrid)'.format(float(self))

class PixelW(float):
    def __str__(self):
        return '{}pixelW'.format(float(self))

    def __repr__(self):
        return str(self)

    def export(self):
        return '({} * pixelW * pixelGrid)'.format(float(self))

class Percentage(float): pass