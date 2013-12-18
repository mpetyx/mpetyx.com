__author__ = 'mpetyx'

from django.contrib.gis.db import models

from mapentity.models import MapEntityMixin


class Museum(MapEntityMixin, models.Model):

    geom = models.PointField()
    name = models.CharField(max_length=80)

    objects = models.GeoManager()

    class Meta:
         app_label = 'museum'