
from .base import customizer
from .display import DisplayModel

class ResourceModel(DisplayModel):
    @customizer(10e10)
    def duration(self, k, value):
        return value
