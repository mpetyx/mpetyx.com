__author__ = 'mpetyx'


from mapentity.views.generic import MapEntityList
from mapentity.views.generic import MapEntityLayer
from mapentity.views.generic import MapEntityJsonList
from mapentity.views.generic import MapEntityDetail
from mapentity.views.generic import MapEntityFormat
from .models import Museum
from .filters import MuseumFilter


class MuseumList(MapEntityList):

    model = Museum
    filterform = MuseumFilter
    columns = ['id', 'name']#, 'atmosphere']


class MuseumLayer(MapEntityLayer):

    model = Museum


class MuseumJsonList(MapEntityJsonList, MuseumList):
    pass


class MuseumDetail(MapEntityDetail):

    model = Museum


class MuseumFormat(MapEntityFormat):

    model = Museum