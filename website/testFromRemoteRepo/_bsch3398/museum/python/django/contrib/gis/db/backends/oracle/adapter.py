from django.contrib.gis.db.backends.adapter import WKTAdapter

from cx_Oracle import CLOB


class OracleSpatialAdapter(WKTAdapter):
    input_size = CLOB
