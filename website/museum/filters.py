__author__ = 'mpetyx'

from .models import Museum
from mapentity.filters import MapEntityFilterSet


class MuseumFilter(MapEntityFilterSet):

    class Meta:
        model = Museum
        fields = ('name', 'atmosphere')