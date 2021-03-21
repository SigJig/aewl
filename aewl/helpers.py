
class EmptyFactor:
    """
    Empty factors, such as safeZoneX which do not get multiplied by anything
    """
    def __str__(self):
        return type(self).__name__

    def __repr__(self):
        return str(self)

    def _operation_skip_if(self, skipper, other, op):
        if other == skipper:
            return self

        return Operation(self, other, op)

    def __mul__(self, other):
        return self._operation_skip_if(1, other, '*')

    def __truediv__(self, other):
        return self._operation_skip_if(1, other, '/')

    def __mod__(self, other):
        return Operation(self, other, '%')

    def __add__(self, other):
        return self._operation_skip_if(0, other, '+')

    def __sub__(self, other):
        return self._operation_skip_if(0, other, '-')

class Factor(EmptyFactor, float):
    def __str__(self):
        return '{}({})'.format(type(self).__name__, float(self))

class Operation(EmptyFactor):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def export(self):
        def _xport(x):
            if hasattr(x, 'export'):
                return x.export()

            return x

        return '({left}{op}{right})'.format(
            left=_xport(self.left),
            op=self.op,
            right=_xport(self.right)
        )

    def __str__(self):
        return '{name}({left}{op}{right})'.format(
            name=type(self).__name__,
            left=self.left,
            op=self.op,
            right=self.right
        )

class SafeZoneX(EmptyFactor):
    def export(self):
        return 'safeZoneX'

class SafeZoneY(EmptyFactor):
    def export(self):
        return 'safeZoneY'

class PixelGrid(EmptyFactor):
    @classmethod
    def pixel_h(cls, fac):
        return Operation(PixelH(fac), cls(), '*')

    @classmethod
    def pixel_w(cls, fac):
        return Operation(PixelW(fac), cls(), '*')

    def export(self):
        return 'pixelGrid'

class SafeZoneW(Factor):
    def export(self):
        return '({} * safeZoneW)'.format(float(self))

class SafeZoneH(Factor):
    def export(self):
        return '({} * safeZoneH)'.format(float(self))

class PixelH(Factor):
    def export(self):
        return '({} * pixelH)'.format(float(self))

class PixelW(Factor):
    def export(self):
        return '({} * pixelW)'.format(float(self))

class Percentage(float): pass