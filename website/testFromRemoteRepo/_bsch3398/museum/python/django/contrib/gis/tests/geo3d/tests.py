import os
import re
import unittest

from django.contrib.gis.db.models import Union, Extent3D
from django.contrib.gis.geos import GEOSGeometry, Point, Polygon
from django.contrib.gis.utils import LayerMapping, LayerMapError

from models import City3D, Interstate2D, Interstate3D, \
    InterstateProj2D, InterstateProj3D, \
    MultiPoint3D, Polygon2D, Polygon3D


data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data'))
city_file = os.path.join(data_path, 'cities', 'cities.shp')
vrt_file = os.path.join(data_path, 'test_vrt', 'test_vrt.vrt')

# The coordinates of each city, with Z values corresponding to their
# altitude in meters.
city_data = (
    ('Houston', (-95.363151, 29.763374, 18)),
    ('Dallas', (-96.801611, 32.782057, 147)),
    ('Oklahoma City', (-97.521157, 34.464642, 380)),
    ('Wellington', (174.783117, -41.315268, 14)),
    ('Pueblo', (-104.609252, 38.255001, 1433)),
    ('Lawrence', (-95.235060, 38.971823, 251)),
    ('Chicago', (-87.650175, 41.850385, 181)),
    ('Victoria', (-123.305196, 48.462611, 15)),
)

# Reference mapping of city name to its altitude (Z value).
city_dict = dict((name, coords) for name, coords in city_data)

# 3D freeway data derived from the National Elevation Dataset: 
#  http://seamless.usgs.gov/products/9arc.php
interstate_data = (
    ('I-45',
     'LINESTRING(-95.3708481 29.7765870 11.339,-95.3694580 29.7787980 4.536,-95.3690305 29.7797359 9.762,-95.3691886 29.7812450 12.448,-95.3696447 29.7850144 10.457,-95.3702511 29.7868518 9.418,-95.3706724 29.7881286 14.858,-95.3711632 29.7896157 15.386,-95.3714525 29.7936267 13.168,-95.3717848 29.7955007 15.104,-95.3717719 29.7969804 16.516,-95.3717305 29.7982117 13.923,-95.3717254 29.8000778 14.385,-95.3719875 29.8013539 15.160,-95.3720575 29.8026785 15.544,-95.3721321 29.8040912 14.975,-95.3722074 29.8050998 15.688,-95.3722779 29.8060430 16.099,-95.3733818 29.8076750 15.197,-95.3741563 29.8103686 17.268,-95.3749458 29.8129927 19.857,-95.3763564 29.8144557 15.435)',
     ( 11.339, 4.536, 9.762, 12.448, 10.457, 9.418, 14.858,
       15.386, 13.168, 15.104, 16.516, 13.923, 14.385, 15.16,
       15.544, 14.975, 15.688, 16.099, 15.197, 17.268, 19.857,
       15.435),
    ),
)

# Bounding box polygon for inner-loop of Houston (in projected coordinate
# system 32140), with elevation values from the National Elevation Dataset
# (see above).
bbox_wkt = 'POLYGON((941527.97 4225693.20,962596.48 4226349.75,963152.57 4209023.95,942051.75 4208366.38,941527.97 4225693.20))'
bbox_z = (21.71, 13.21, 9.12, 16.40, 21.71)


def gen_bbox():
    bbox_2d = GEOSGeometry(bbox_wkt, srid=32140)
    bbox_3d = Polygon(tuple((x, y, z) for (x, y), z in zip(bbox_2d[0].coords, bbox_z)), srid=32140)
    return bbox_2d, bbox_3d


class Geo3DTest(unittest.TestCase):
    """
    Only a subset of the PostGIS routines are 3D-enabled, and this TestCase
    tries to test the features that can handle 3D and that are also 
    available within GeoDjango.  For more information, see the PostGIS docs
    on the routines that support 3D:

    http://postgis.refractions.net/documentation/manual-1.4/ch08.html#PostGIS_3D_Functions
    """

    def test01_3d(self):
        "Test the creation of 3D models."
        # 3D models for the rest of the tests will be populated in here.
        # For each 3D data set create model (and 2D version if necessary), 
        # retrieve, and assert geometry is in 3D and contains the expected
        # 3D values.
        for name, pnt_data in city_data:
            x, y, z = pnt_data
            pnt = Point(x, y, z, srid=4326)
            City3D.objects.create(name=name, point=pnt)
            city = City3D.objects.get(name=name)
            self.failUnless(city.point.hasz)
            self.assertEqual(z, city.point.z)

        # Interstate (2D / 3D and Geographic/Projected variants)
        for name, line, exp_z in interstate_data:
            line_3d = GEOSGeometry(line, srid=4269)
            # Using `hex` attribute because it omits 3D.
            line_2d = GEOSGeometry(line_3d.hex, srid=4269)

            # Creating a geographic and projected version of the
            # interstate in both 2D and 3D.
            Interstate3D.objects.create(name=name, line=line_3d)
            InterstateProj3D.objects.create(name=name, line=line_3d)
            Interstate2D.objects.create(name=name, line=line_2d)
            InterstateProj2D.objects.create(name=name, line=line_2d)

            # Retrieving and making sure it's 3D and has expected
            # Z values -- shouldn't change because of coordinate system.
            interstate = Interstate3D.objects.get(name=name)
            interstate_proj = InterstateProj3D.objects.get(name=name)
            for i in [interstate, interstate_proj]:
                self.failUnless(i.line.hasz)
                self.assertEqual(exp_z, tuple(i.line.z))

        # Creating 3D Polygon.
        bbox2d, bbox3d = gen_bbox()
        Polygon2D.objects.create(name='2D BBox', poly=bbox2d)
        Polygon3D.objects.create(name='3D BBox', poly=bbox3d)
        p3d = Polygon3D.objects.get(name='3D BBox')
        self.failUnless(p3d.poly.hasz)
        self.assertEqual(bbox3d, p3d.poly)

    def test01a_3d_layermapping(self):
        "Testing LayerMapping on 3D models."
        from models import Point2D, Point3D

        point_mapping = {'point': 'POINT'}
        mpoint_mapping = {'mpoint': 'MULTIPOINT'}

        # The VRT is 3D, but should still be able to map sans the Z.
        lm = LayerMapping(Point2D, vrt_file, point_mapping, transform=False)
        lm.save()
        self.assertEqual(3, Point2D.objects.count())

        # The city shapefile is 2D, and won't be able to fill the coordinates
        # in the 3D model -- thus, a LayerMapError is raised.
        self.assertRaises(LayerMapError, LayerMapping,
                          Point3D, city_file, point_mapping, transform=False)

        # 3D model should take 3D data just fine.
        lm = LayerMapping(Point3D, vrt_file, point_mapping, transform=False)
        lm.save()
        self.assertEqual(3, Point3D.objects.count())

        # Making sure LayerMapping.make_multi works right, by converting
        # a Point25D into a MultiPoint25D.
        lm = LayerMapping(MultiPoint3D, vrt_file, mpoint_mapping, transform=False)
        lm.save()
        self.assertEqual(3, MultiPoint3D.objects.count())

    def test02a_kml(self):
        "Test GeoQuerySet.kml() with Z values."
        h = City3D.objects.kml(precision=6).get(name='Houston')
        # KML should be 3D.
        # `SELECT ST_AsKML(point, 6) FROM geo3d_city3d WHERE name = 'Houston';`
        ref_kml_regex = re.compile(r'^<Point><coordinates>-95.363\d+,29.763\d+,18</coordinates></Point>$')
        self.failUnless(ref_kml_regex.match(h.kml))

    def test02b_geojson(self):
        "Test GeoQuerySet.geojson() with Z values."
        h = City3D.objects.geojson(precision=6).get(name='Houston')
        # GeoJSON should be 3D
        # `SELECT ST_AsGeoJSON(point, 6) FROM geo3d_city3d WHERE name='Houston';`
        ref_json_regex = re.compile(r'^{"type":"Point","coordinates":\[-95.363151,29.763374,18(\.0+)?\]}$')
        self.failUnless(ref_json_regex.match(h.geojson))

    def test03a_union(self):
        "Testing the Union aggregate of 3D models."
        # PostGIS query that returned the reference EWKT for this test:
        #  `SELECT ST_AsText(ST_Union(point)) FROM geo3d_city3d;`
        ref_ewkt = 'SRID=4326;MULTIPOINT(-123.305196 48.462611 15,-104.609252 38.255001 1433,-97.521157 34.464642 380,-96.801611 32.782057 147,-95.363151 29.763374 18,-95.23506 38.971823 251,-87.650175 41.850385 181,174.783117 -41.315268 14)'
        ref_union = GEOSGeometry(ref_ewkt)
        union = City3D.objects.aggregate(Union('point'))['point__union']
        self.failUnless(union.hasz)
        self.assertEqual(ref_union, union)

    def test03b_extent(self):
        "Testing the Extent3D aggregate for 3D models."
        # `SELECT ST_Extent3D(point) FROM geo3d_city3d;`
        ref_extent3d = (-123.305196, -41.315268, 14, 174.783117, 48.462611, 1433)
        extent1 = City3D.objects.aggregate(Extent3D('point'))['point__extent3d']
        extent2 = City3D.objects.extent3d()

        def check_extent3d(extent3d, tol=6):
            for ref_val, ext_val in zip(ref_extent3d, extent3d):
                self.assertAlmostEqual(ref_val, ext_val, tol)

        for e3d in [extent1, extent2]:
            check_extent3d(e3d)

    def test04_perimeter(self):
        "Testing GeoQuerySet.perimeter() on 3D fields."
        # Reference query for values below:
        #  `SELECT ST_Perimeter3D(poly), ST_Perimeter2D(poly) FROM geo3d_polygon3d;`
        ref_perim_3d = 76859.2620451
        ref_perim_2d = 76859.2577803
        tol = 6
        self.assertAlmostEqual(ref_perim_2d,
                               Polygon2D.objects.perimeter().get(name='2D BBox').perimeter.m,
                               tol)
        self.assertAlmostEqual(ref_perim_3d,
                               Polygon3D.objects.perimeter().get(name='3D BBox').perimeter.m,
                               tol)

    def test05_length(self):
        "Testing GeoQuerySet.length() on 3D fields."
        # ST_Length_Spheroid Z-aware, and thus does not need to use
        # a separate function internally.
        # `SELECT ST_Length_Spheroid(line, 'SPHEROID["GRS 1980",6378137,298.257222101]') 
        #    FROM geo3d_interstate[2d|3d];`
        tol = 3
        ref_length_2d = 4368.1721949481
        ref_length_3d = 4368.62547052088
        self.assertAlmostEqual(ref_length_2d,
                               Interstate2D.objects.length().get(name='I-45').length.m,
                               tol)
        self.assertAlmostEqual(ref_length_3d,
                               Interstate3D.objects.length().get(name='I-45').length.m,
                               tol)

        # Making sure `ST_Length3D` is used on for a projected
        # and 3D model rather than `ST_Length`.
        # `SELECT ST_Length(line) FROM geo3d_interstateproj2d;`
        ref_length_2d = 4367.71564892392
        # `SELECT ST_Length3D(line) FROM geo3d_interstateproj3d;`
        ref_length_3d = 4368.16897234101
        self.assertAlmostEqual(ref_length_2d,
                               InterstateProj2D.objects.length().get(name='I-45').length.m,
                               tol)
        self.assertAlmostEqual(ref_length_3d,
                               InterstateProj3D.objects.length().get(name='I-45').length.m,
                               tol)

    def test06_scale(self):
        "Testing GeoQuerySet.scale() on Z values."
        # Mapping of City name to reference Z values.
        zscales = (-3, 4, 23)
        for zscale in zscales:
            for city in City3D.objects.scale(1.0, 1.0, zscale):
                self.assertEqual(city_dict[city.name][2] * zscale, city.scale.z)

    def test07_translate(self):
        "Testing GeoQuerySet.translate() on Z values."
        ztranslations = (5.23, 23, -17)
        for ztrans in ztranslations:
            for city in City3D.objects.translate(0, 0, ztrans):
                self.assertEqual(city_dict[city.name][2] + ztrans, city.translate.z)


def suite():
    s = unittest.TestSuite()
    s.addTest(unittest.makeSuite(Geo3DTest))
    return s
