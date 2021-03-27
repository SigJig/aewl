
from .base import customizer
from .display import Display

class Resource(Display):
    @customizer(10e10)
    def duration(self, k, value):
        return value