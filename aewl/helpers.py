
class PixelH(float):
    def export(self):
        return '({} * pixelH * pixelGrid)'.format(self)

class PixelW(float):
    def export(self):
        return '({} * pixelW * pixelGrid)'.format(self)

class Percentage(float): pass