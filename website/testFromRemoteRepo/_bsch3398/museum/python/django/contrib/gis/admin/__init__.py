# Getting the normal admin routines, classes, and `site` instance.

# Geographic admin options classes and widgets.

try:
    from django.contrib.gis.admin.options import OSMGeoAdmin

    HAS_OSM = True
except ImportError:
    HAS_OSM = False
