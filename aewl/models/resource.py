
from .base import customizer
from .display import DisplayModel

class ResourceModel(DisplayModel):
    fields = {
        **DisplayModel.fields,
        'duration': 10e10
    }

    @customizer()
    def duration(self, value):
        return value
