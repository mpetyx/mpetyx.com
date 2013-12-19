import re

wkt_regex = re.compile(r'^(?P<type>[A-Z]+) ?\(')


class TestGeom:
    "The Test Geometry class container."

    def __init__(self, wkt, **kwargs):
        self.wkt = wkt

        self.bad = kwargs.pop('bad', False)

        if not self.bad:
            m = wkt_regex.match(wkt)
            if not m:
                raise Exception('Improper WKT: "%s"' % wkt)
            self.geo_type = m.group('type')

        for key, value in kwargs.items():
            setattr(self, key, value)

# For the old tests
swig_geoms = (TestGeom('POLYGON ((0 0, 0 100, 100 100, 100 0, 0 0))', ncoords=5),
              TestGeom('POLYGON ((0 0, 0 100, 100 100, 100 0, 0 0), (10 10, 10 90, 90 90, 90 10, 10 10) ))',
                       ncoords=10),
)

# Testing WKT & HEX
hex_wkt = (TestGeom('POINT(0 1)', hex='01010000000000000000000000000000000000F03F'),
           TestGeom('LINESTRING(0 1, 2 3, 4 5)',
                    hex='0102000000030000000000000000000000000000000000F03F0000000000000040000000000000084000000000000010400000000000001440'),
           TestGeom('POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))',
                    hex='010300000001000000050000000000000000000000000000000000000000000000000024400000000000000000000000000000244000000000000024400000000000000000000000000000244000000000000000000000000000000000'),
           TestGeom('MULTIPOINT(0 0, 10 0, 10 10, 0 10, 0 0)',
                    hex='010400000005000000010100000000000000000000000000000000000000010100000000000000000024400000000000000000010100000000000000000024400000000000002440010100000000000000000000000000000000002440010100000000000000000000000000000000000000'),
           TestGeom('MULTILINESTRING((0 0, 10 0, 10 10, 0 10),(20 20, 30 20))',
                    hex='01050000000200000001020000000400000000000000000000000000000000000000000000000000244000000000000000000000000000002440000000000000244000000000000000000000000000002440010200000002000000000000000000344000000000000034400000000000003E400000000000003440'),
           TestGeom(
               'MULTIPOLYGON(((0 0, 10 0, 10 10, 0 10, 0 0)),((20 20, 20 30, 30 30, 30 20, 20 20),(25 25, 25 26, 26 26, 26 25, 25 25)))',
               hex='010600000002000000010300000001000000050000000000000000000000000000000000000000000000000024400000000000000000000000000000244000000000000024400000000000000000000000000000244000000000000000000000000000000000010300000002000000050000000000000000003440000000000000344000000000000034400000000000003E400000000000003E400000000000003E400000000000003E40000000000000344000000000000034400000000000003440050000000000000000003940000000000000394000000000000039400000000000003A400000000000003A400000000000003A400000000000003A40000000000000394000000000000039400000000000003940'),
           TestGeom(
               'GEOMETRYCOLLECTION(MULTIPOLYGON(((0 0, 10 0, 10 10, 0 10, 0 0)),((20 20, 20 30, 30 30, 30 20, 20 20),(25 25, 25 26, 26 26, 26 25, 25 25))),MULTILINESTRING((0 0, 10 0, 10 10, 0 10),(20 20, 30 20)),MULTIPOINT(0 0, 10 0, 10 10, 0 10, 0 0))',
               hex='010700000003000000010600000002000000010300000001000000050000000000000000000000000000000000000000000000000024400000000000000000000000000000244000000000000024400000000000000000000000000000244000000000000000000000000000000000010300000002000000050000000000000000003440000000000000344000000000000034400000000000003E400000000000003E400000000000003E400000000000003E40000000000000344000000000000034400000000000003440050000000000000000003940000000000000394000000000000039400000000000003A400000000000003A400000000000003A400000000000003A4000000000000039400000000000003940000000000000394001050000000200000001020000000400000000000000000000000000000000000000000000000000244000000000000000000000000000002440000000000000244000000000000000000000000000002440010200000002000000000000000000344000000000000034400000000000003E400000000000003440010400000005000000010100000000000000000000000000000000000000010100000000000000000024400000000000000000010100000000000000000024400000000000002440010100000000000000000000000000000000002440010100000000000000000000000000000000000000'),
)

# WKT, GML, KML output
wkt_out = (TestGeom('POINT (110 130)', ewkt='POINT (110.0000000000000000 130.0000000000000000)',
                    kml='<Point><coordinates>110.0,130.0,0</coordinates></Point>',
                    gml='<gml:Point><gml:coordinates>110,130</gml:coordinates></gml:Point>'),
           TestGeom('LINESTRING (40 40,50 130,130 130)',
                    ewkt='LINESTRING (40.0000000000000000 40.0000000000000000, 50.0000000000000000 130.0000000000000000, 130.0000000000000000 130.0000000000000000)',
                    kml='<LineString><coordinates>40.0,40.0,0 50.0,130.0,0 130.0,130.0,0</coordinates></LineString>',
                    gml='<gml:LineString><gml:coordinates>40,40 50,130 130,130</gml:coordinates></gml:LineString>'),
           TestGeom('POLYGON ((150 150,410 150,280 20,20 20,150 150),(170 120,330 120,260 50,100 50,170 120))',
                    ewkt='POLYGON ((150.0000000000000000 150.0000000000000000, 410.0000000000000000 150.0000000000000000, 280.0000000000000000 20.0000000000000000, 20.0000000000000000 20.0000000000000000, 150.0000000000000000 150.0000000000000000), (170.0000000000000000 120.0000000000000000, 330.0000000000000000 120.0000000000000000, 260.0000000000000000 50.0000000000000000, 100.0000000000000000 50.0000000000000000, 170.0000000000000000 120.0000000000000000))',
                    kml='<Polygon><outerBoundaryIs><LinearRing><coordinates>150.0,150.0,0 410.0,150.0,0 280.0,20.0,0 20.0,20.0,0 150.0,150.0,0</coordinates></LinearRing></outerBoundaryIs><innerBoundaryIs><LinearRing><coordinates>170.0,120.0,0 330.0,120.0,0 260.0,50.0,0 100.0,50.0,0 170.0,120.0,0</coordinates></LinearRing></innerBoundaryIs></Polygon>',
                    gml='<gml:Polygon><gml:outerBoundaryIs><gml:LinearRing><gml:coordinates>150,150 410,150 280,20 20,20 150,150</gml:coordinates></gml:LinearRing></gml:outerBoundaryIs><gml:innerBoundaryIs><gml:LinearRing><gml:coordinates>170,120 330,120 260,50 100,50 170,120</gml:coordinates></gml:LinearRing></gml:innerBoundaryIs></gml:Polygon>'),
           TestGeom('MULTIPOINT (10 80,110 170,110 120)',
                    ewkt='MULTIPOINT (10.0000000000000000 80.0000000000000000, 110.0000000000000000 170.0000000000000000, 110.0000000000000000 120.0000000000000000)',
                    kml='<MultiGeometry><Point><coordinates>10.0,80.0,0</coordinates></Point><Point><coordinates>110.0,170.0,0</coordinates></Point><Point><coordinates>110.0,120.0,0</coordinates></Point></MultiGeometry>',
                    gml='<gml:MultiPoint><gml:pointMember><gml:Point><gml:coordinates>10,80</gml:coordinates></gml:Point></gml:pointMember><gml:pointMember><gml:Point><gml:coordinates>110,170</gml:coordinates></gml:Point></gml:pointMember><gml:pointMember><gml:Point><gml:coordinates>110,120</gml:coordinates></gml:Point></gml:pointMember></gml:MultiPoint>'),
           TestGeom('MULTILINESTRING ((110 100,40 30,180 30),(170 30,110 90,50 30))',
                    ewkt='MULTILINESTRING ((110.0000000000000000 100.0000000000000000, 40.0000000000000000 30.0000000000000000, 180.0000000000000000 30.0000000000000000), (170.0000000000000000 30.0000000000000000, 110.0000000000000000 90.0000000000000000, 50.0000000000000000 30.0000000000000000))',
                    kml='<MultiGeometry><LineString><coordinates>110.0,100.0,0 40.0,30.0,0 180.0,30.0,0</coordinates></LineString><LineString><coordinates>170.0,30.0,0 110.0,90.0,0 50.0,30.0,0</coordinates></LineString></MultiGeometry>',
                    gml='<gml:MultiLineString><gml:lineStringMember><gml:LineString><gml:coordinates>110,100 40,30 180,30</gml:coordinates></gml:LineString></gml:lineStringMember><gml:lineStringMember><gml:LineString><gml:coordinates>170,30 110,90 50,30</gml:coordinates></gml:LineString></gml:lineStringMember></gml:MultiLineString>'),
           TestGeom(
               'MULTIPOLYGON (((110 110,70 200,150 200,110 110),(110 110,100 180,120 180,110 110)),((110 110,150 20,70 20,110 110),(110 110,120 40,100 40,110 110)))',
               ewkt='MULTIPOLYGON (((110.0000000000000000 110.0000000000000000, 70.0000000000000000 200.0000000000000000, 150.0000000000000000 200.0000000000000000, 110.0000000000000000 110.0000000000000000), (110.0000000000000000 110.0000000000000000, 100.0000000000000000 180.0000000000000000, 120.0000000000000000 180.0000000000000000, 110.0000000000000000 110.0000000000000000)), ((110.0000000000000000 110.0000000000000000, 150.0000000000000000 20.0000000000000000, 70.0000000000000000 20.0000000000000000, 110.0000000000000000 110.0000000000000000), (110.0000000000000000 110.0000000000000000, 120.0000000000000000 40.0000000000000000, 100.0000000000000000 40.0000000000000000, 110.0000000000000000 110.0000000000000000)))',
               kml='<MultiGeometry><Polygon><outerBoundaryIs><LinearRing><coordinates>110.0,110.0,0 70.0,200.0,0 150.0,200.0,0 110.0,110.0,0</coordinates></LinearRing></outerBoundaryIs><innerBoundaryIs><LinearRing><coordinates>110.0,110.0,0 100.0,180.0,0 120.0,180.0,0 110.0,110.0,0</coordinates></LinearRing></innerBoundaryIs></Polygon><Polygon><outerBoundaryIs><LinearRing><coordinates>110.0,110.0,0 150.0,20.0,0 70.0,20.0,0 110.0,110.0,0</coordinates></LinearRing></outerBoundaryIs><innerBoundaryIs><LinearRing><coordinates>110.0,110.0,0 120.0,40.0,0 100.0,40.0,0 110.0,110.0,0</coordinates></LinearRing></innerBoundaryIs></Polygon></MultiGeometry>',
               gml='<gml:MultiPolygon><gml:polygonMember><gml:Polygon><gml:outerBoundaryIs><gml:LinearRing><gml:coordinates>110,110 70,200 150,200 110,110</gml:coordinates></gml:LinearRing></gml:outerBoundaryIs><gml:innerBoundaryIs><gml:LinearRing><gml:coordinates>110,110 100,180 120,180 110,110</gml:coordinates></gml:LinearRing></gml:innerBoundaryIs></gml:Polygon></gml:polygonMember><gml:polygonMember><gml:Polygon><gml:outerBoundaryIs><gml:LinearRing><gml:coordinates>110,110 150,20 70,20 110,110</gml:coordinates></gml:LinearRing></gml:outerBoundaryIs><gml:innerBoundaryIs><gml:LinearRing><gml:coordinates>110,110 120,40 100,40 110,110</gml:coordinates></gml:LinearRing></gml:innerBoundaryIs></gml:Polygon></gml:polygonMember></gml:MultiPolygon>'),
           TestGeom('GEOMETRYCOLLECTION (POINT (110 260),LINESTRING (110 0,110 60))',
                    ewkt='GEOMETRYCOLLECTION (POINT (110.0000000000000000 260.0000000000000000), LINESTRING (110.0000000000000000 0.0000000000000000, 110.0000000000000000 60.0000000000000000))',
                    kml='<MultiGeometry><Point><coordinates>110.0,260.0,0</coordinates></Point><LineString><coordinates>110.0,0.0,0 110.0,60.0,0</coordinates></LineString></MultiGeometry>',
                    gml='<gml:GeometryCollection><gml:geometryMember><gml:Point><gml:coordinates>110,260</gml:coordinates></gml:Point></gml:geometryMember><gml:geometryMember><gml:LineString><gml:coordinates>110,0 110,60</gml:coordinates></gml:LineString></gml:geometryMember></gml:GeometryCollection>'),
)

# Errors
errors = (TestGeom('GEOMETR##!@#%#............a32515', bad=True, hex=False),
          TestGeom('Foo.Bar', bad=True, hex=False),
          TestGeom('POINT (5, 23)', bad=True, hex=False),
          TestGeom('AAABBBDDDAAD##@#1113511111-098111111111111111533333333333333', bad=True, hex=True),
          TestGeom('FFFFFFFFFFFFFFFFF1355555555555555555565111', bad=True, hex=True),
          TestGeom('', bad=True, hex=False),
)

# Polygons
polygons = (TestGeom('POLYGON ((0 0, 0 100, 100 100, 100 0, 0 0), (10 10, 10 90, 90 90, 90 10, 10 10))',
                     n_i=1, ext_ring_cs=((0, 0), (0, 100), (100, 100), (100, 0), (0, 0)), n_p=10, area=3600.0,
                     centroid=(50., 50.),
),
            TestGeom(
                'POLYGON ((0 0, 0 100, 100 100, 100 0, 0 0), (10 10, 10 20, 20 20, 20 10, 10 10), (80 80, 80 90, 90 90, 90 80, 80 80))',
                n_i=2, ext_ring_cs=((0, 0), (0, 100), (100, 100), (100, 0), (0, 0)), n_p=15, area=9800.0,
                centroid=(50., 50.),
            ),
            TestGeom('POLYGON ((0 0, 0 100, 100 100, 100 0, 0 0))',
                     n_i=0, ext_ring_cs=((0, 0), (0, 100), (100, 100), (100, 0), (0, 0)), n_p=5, area=10000.0,
                     centroid=(50., 50.),
            ),
            TestGeom(
                'POLYGON ((-95.3848703124799471 29.7056021479768511, -95.3851905195191847 29.7046588196500281, -95.3859356966379011 29.7025053545605502, -95.3860723000647539 29.7020963367038391, -95.3871517697222089 29.6989779021280995, -95.3865578518265522 29.6990856888057202, -95.3862634205175226 29.6999471753441782, -95.3861991779541967 29.6999591988978615, -95.3856773799358137 29.6998323107113578, -95.3856209915427229 29.6998005235473741, -95.3855833545501639 29.6996619391729801, -95.3855776331865002 29.6996232659570047, -95.3850162731712885 29.6997236706530536, -95.3831047357410284 29.7000847603095082, -95.3829800724914776 29.7000676365023502, -95.3828084594470909 29.6999969684031200, -95.3828131504821499 29.6999090511531065, -95.3828022942979601 29.6998152117366025, -95.3827893930918833 29.6997790953076759, -95.3825174668099862 29.6998267772748825, -95.3823521544804862 29.7000451723151606, -95.3820491918785223 29.6999682034582335, -95.3817932841505893 29.6999640407204772, -95.3815438924600443 29.7005983712500630, -95.3807812390843424 29.7007538492921590, -95.3778578936435935 29.7012966201172048, -95.3770817300034679 29.7010555145969093, -95.3772763716395957 29.7004995005932031, -95.3769891024414420 29.7005797730360186, -95.3759855007185990 29.7007754783987821, -95.3759516423090474 29.7007305400669388, -95.3765252155960042 29.6989549173240874, -95.3766842746727832 29.6985134987163164, -95.3768510987262914 29.6980530300744938, -95.3769198676258014 29.6977137204527573, -95.3769616670751930 29.6973351617272172, -95.3770309229297766 29.6969821084304186, -95.3772352596880637 29.6959751305871613, -95.3776232419333354 29.6945439060847463, -95.3776849628727064 29.6943364710766069, -95.3779699491714723 29.6926548349458947, -95.3781945479573494 29.6920088336742545, -95.3785807118394189 29.6908279316076005, -95.3787441368896651 29.6908846275832197, -95.3787903214163890 29.6907152912461640, -95.3791765069353659 29.6893335376821526, -95.3794935959513026 29.6884781789101595, -95.3796592071232112 29.6880066681407619, -95.3799788182090111 29.6873687353035081, -95.3801545516183893 29.6868782380716993, -95.3801258908302145 29.6867756621337762, -95.3801104284899566 29.6867229678809572, -95.3803803523746154 29.6863753372986459, -95.3821028558287622 29.6837392961470421, -95.3827289584682205 29.6828097375216160, -95.3827494698109035 29.6790739156259278, -95.3826022014838486 29.6776502228345507, -95.3825047356438063 29.6765773006280753, -95.3823473035336917 29.6750405250369127, -95.3824540163482055 29.6750076408228587, -95.3838984230304305 29.6745679207378679, -95.3916547074937426 29.6722459226508377, -95.3926154662749468 29.6719609085105489, -95.3967246645118081 29.6707316485589736, -95.3974588054406780 29.6705065336410989, -95.3978523748756828 29.6703795547846845, -95.3988598162279970 29.6700874981900853, -95.3995628600665952 29.6698505300412414, -95.4134721665944170 29.6656841279906232, -95.4143262068232616 29.6654291174019278, -95.4159685142480214 29.6649750989232288, -95.4180067396277565 29.6643253024318021, -95.4185886692196590 29.6641482768691063, -95.4234155309609662 29.6626925393704788, -95.4287785503196346 29.6611023620959706, -95.4310287312749352 29.6604222580752648, -95.4320295629628959 29.6603361318136720, -95.4332899683975739 29.6600560661713608, -95.4342675748811047 29.6598454934599900, -95.4343110414310871 29.6598411486215490, -95.4345576779282538 29.6598147020668499, -95.4348823041721630 29.6597875803673112, -95.4352827715209457 29.6597762346946681, -95.4355290431309982 29.6597827926562374, -95.4359197997999331 29.6598014511782715, -95.4361907884752156 29.6598444333523368, -95.4364608955807228 29.6598901433108217, -95.4367250147512323 29.6599494499910712, -95.4364898759758091 29.6601880616540186, -95.4354501111810691 29.6616378572201107, -95.4381459623171224 29.6631265631655126, -95.4367852490863129 29.6642266600024023, -95.4370040894557263 29.6643425389568769, -95.4367078350812648 29.6645492592343238, -95.4366081749871285 29.6646291473027297, -95.4358539359938192 29.6652308742342932, -95.4350327668927889 29.6658995989314462, -95.4350580905272921 29.6678812477895271, -95.4349710541447536 29.6680054925936965, -95.4349500440473548 29.6671410080890006, -95.4341492724148850 29.6678790545191688, -95.4340248868274728 29.6680353198492135, -95.4333227845797438 29.6689245624945990, -95.4331325652123326 29.6691616138940901, -95.4321314741096955 29.6704473333237253, -95.4320435792664341 29.6702578985411982, -95.4320147929883547 29.6701800936425109, -95.4319764538662980 29.6683246590817085, -95.4317490976340679 29.6684974372577166, -95.4305958185342718 29.6694049049170374, -95.4296600735653016 29.6701723430938493, -95.4284928989940937 29.6710931793380972, -95.4274630532378580 29.6719378813640091, -95.4273056811974811 29.6720684984625791, -95.4260554084574864 29.6730668861566969, -95.4253558063699643 29.6736342467365724, -95.4249278826026028 29.6739557343648919, -95.4248648873821423 29.6745400910786152, -95.4260016131471929 29.6750987014005858, -95.4258567183010911 29.6753452063069929, -95.4260238081486847 29.6754322077221353, -95.4258707374502393 29.6756647377294307, -95.4257951755816691 29.6756407098663360, -95.4257701599566985 29.6761077719536068, -95.4257726684792260 29.6761711204603955, -95.4257980187195614 29.6770219651929423, -95.4252712669032519 29.6770161558853758, -95.4249234392992065 29.6770068683962300, -95.4249574272905789 29.6779707498635759, -95.4244725881033702 29.6779825646764159, -95.4222269476429545 29.6780711474441716, -95.4223032371999267 29.6796029391538809, -95.4239133706588945 29.6795331493690355, -95.4224579084327331 29.6813706893847780, -95.4224290108823965 29.6821953228763924, -95.4230916478977349 29.6822130268724109, -95.4222928279595521 29.6832041816675343, -95.4228763710016352 29.6832087677714505, -95.4223401691637179 29.6838987872753748, -95.4211655906087088 29.6838784024852984, -95.4201984153205558 29.6851319258758082, -95.4206156387716362 29.6851623398125319, -95.4213438084897660 29.6851763011334739, -95.4212071118618752 29.6853679931624974, -95.4202651399651245 29.6865313962980508, -95.4172061157659783 29.6865816431043932, -95.4182217951255183 29.6872251197301544, -95.4178664826439160 29.6876750901471631, -95.4180678442928780 29.6877960336377207, -95.4188763472917572 29.6882826379510938, -95.4185374500596311 29.6887137897831934, -95.4182121713132290 29.6885097429738813, -95.4179857231741551 29.6888118367840086, -95.4183106010563620 29.6890048676118212, -95.4179489865331334 29.6894546700979056, -95.4175581746284820 29.6892323606815438, -95.4173439957341571 29.6894990139807007, -95.4177411199311081 29.6897435034738422, -95.4175789200209721 29.6899207529979208, -95.4170598559864800 29.6896042165807508, -95.4166733682539814 29.6900891174451367, -95.4165941362704331 29.6900347214235047, -95.4163537218065301 29.6903529467753238, -95.4126843270708775 29.6881086357212780, -95.4126604121378392 29.6880942378803496, -95.4126672298953338 29.6885951670109982, -95.4126680884821923 29.6887052446594275, -95.4158080137241882 29.6906382377959339, -95.4152061403821961 29.6910871045531586, -95.4155842583188161 29.6917382915894308, -95.4157426793520358 29.6920726941677096, -95.4154520563662203 29.6922052332446427, -95.4151389936167078 29.6923261661269571, -95.4148649784384872 29.6924343866430256, -95.4144051352401590 29.6925623927348106, -95.4146792019416665 29.6926770338507744, -95.4148824479948985 29.6928117893696388, -95.4149851734360226 29.6929823719519774, -95.4140436551925291 29.6929626643100946, -95.4140465993023241 29.6926545917254892, -95.4137269186733334 29.6927395764256090, -95.4137372859685513 29.6935432485666624, -95.4135702836218655 29.6933186678088283, -95.4133925235973237 29.6930415229852152, -95.4133017035615580 29.6928685062036166, -95.4129588921634593 29.6929391128977862, -95.4125107395559695 29.6930481664661485, -95.4102647423187307 29.6935850183258019, -95.4081931340840157 29.6940907430947760, -95.4078783596459772 29.6941703429951609, -95.4049213975000043 29.6948723732981961, -95.4045944244127071 29.6949626434239207, -95.4045865139788134 29.6954109019001358, -95.4045953345484037 29.6956972800496963, -95.4038879332535146 29.6958296089365490, -95.4040366394459340 29.6964389004769842, -95.4032774779020798 29.6965643341263892, -95.4026066501239853 29.6966646227683881, -95.4024991226393837 29.6961389766619703, -95.4011781398631911 29.6963566063186377, -95.4011524097636112 29.6962596176762190, -95.4018184046368276 29.6961399466727336, -95.4016995838361908 29.6956442609415099, -95.4007100753964608 29.6958900524002978, -95.4008032469935188 29.6962639900781404, -95.3995660267125487 29.6965636449370329, -95.3996140564775601 29.6967877962763644, -95.3996364430014410 29.6968901984825280, -95.3984003269631842 29.6968679634805746, -95.3981442026887265 29.6983660679730335, -95.3980178461957706 29.6990890276252415, -95.3977097967130163 29.7008526152273049, -95.3962347157626027 29.7009697553607630, -95.3951949050136250 29.7004740386619019, -95.3957564950617183 29.6990281830553187, -95.3965927101519924 29.6968771129030706, -95.3957496517238184 29.6970800358387095, -95.3957720559467361 29.6972264611230727, -95.3957391586571788 29.6973548894558732, -95.3956286413405365 29.6974949857280883, -95.3955111053256957 29.6975661086270186, -95.3953215342724121 29.6976022763384790, -95.3951795558443365 29.6975846977491038, -95.3950369632041060 29.6975175779330200, -95.3949401089966500 29.6974269267953304, -95.3948740281415581 29.6972903308506346, -95.3946650813866910 29.6973397326847923, -95.3947654059391112 29.6974882560192022, -95.3949627316619768 29.6980355864961858, -95.3933200807862249 29.6984590863712796, -95.3932606497523494 29.6984464798710839, -95.3932983699113350 29.6983154306484352, -95.3933058014696655 29.6982165816983610, -95.3932946347785133 29.6981089778195759, -95.3931780601756287 29.6977068906794841, -95.3929928222970602 29.6977541771878180, -95.3930873169846478 29.6980676264932946, -95.3932743746374570 29.6981249406449663, -95.3929512584706316 29.6989526513922222, -95.3919850280655197 29.7014358632108646, -95.3918950918929056 29.7014169320765724, -95.3916928317890296 29.7019232352846423, -95.3915424614970959 29.7022988712928289, -95.3901530441668939 29.7058519502930061, -95.3899656322116698 29.7059156823562418, -95.3897628748670883 29.7059900058266777, -95.3896062677805787 29.7060738276384946, -95.3893941800512266 29.7061891695242046, -95.3892150365492455 29.7062641292949436, -95.3890502563035199 29.7063339729630940, -95.3888717930715586 29.7063896908080736, -95.3886925428988945 29.7064453871994978, -95.3885376849411983 29.7064797304524149, -95.3883284158984139 29.7065153575050189, -95.3881046767627794 29.7065368368267357, -95.3878809284696132 29.7065363048447537, -95.3876046356120924 29.7065288525102424, -95.3873060894974714 29.7064822806001452, -95.3869851943158409 29.7063993367575350, -95.3865967896568065 29.7062870572919202, -95.3861785624983156 29.7061492099008184, -95.3857375009733488 29.7059887337478798, -95.3854573290902152 29.7058683664514618, -95.3848703124799471 29.7056021479768511))',
                n_i=0, ext_ring_cs=False, n_p=264, area=0.00129917360654,
                centroid=(-95.403569179437341, 29.681772571690402),
            ),
)

# MultiPolygons
multipolygons = (TestGeom(
    'MULTIPOLYGON (((100 20, 180 20, 180 100, 100 100, 100 20)), ((20 100, 100 100, 100 180, 20 180, 20 100)), ((100 180, 180 180, 180 260, 100 260, 100 180)), ((180 100, 260 100, 260 180, 180 180, 180 100)))',
    valid=True, num_geom=4, n_p=20),
                 TestGeom(
                     'MULTIPOLYGON (((60 300, 320 220, 260 60, 60 100, 60 300)), ((60 300, 320 220, 260 60, 60 100, 60 300)))',
                     valid=False),
                 TestGeom(
                     'MULTIPOLYGON (((180 60, 240 160, 300 60, 180 60)), ((80 80, 180 60, 160 140, 240 160, 360 140, 300 60, 420 100, 320 280, 120 260, 80 80)))',
                     valid=True, num_geom=2, n_p=14),
)

# Points
points = (TestGeom('POINT (5 23)', x=5.0, y=23.0, centroid=(5.0, 23.0)),
          TestGeom('POINT (-95.338492 29.723893)', x=-95.338492, y=29.723893, centroid=(-95.338492, 29.723893)),
          TestGeom('POINT(1.234 5.678)', x=1.234, y=5.678, centroid=(1.234, 5.678)),
          TestGeom('POINT(4.321 8.765)', x=4.321, y=8.765, centroid=(4.321, 8.765)),
          TestGeom('POINT(10 10)', x=10, y=10, centroid=(10., 10.)),
          TestGeom('POINT (5 23 8)', x=5.0, y=23.0, z=8.0, centroid=(5.0, 23.0)),
)

# MultiPoints
multipoints = (TestGeom('MULTIPOINT(10 10, 20 20 )', n_p=2, points=((10., 10.), (20., 20.)), centroid=(15., 15.)),
               TestGeom('MULTIPOINT(10 10, 20 20, 10 20, 20 10)',
                        n_p=4, points=((10., 10.), (20., 20.), (10., 20.), (20., 10.)),
                        centroid=(15., 15.)),
)

# LineStrings
linestrings = (
TestGeom('LINESTRING (60 180, 120 100, 180 180)', n_p=3, centroid=(120, 140), tup=((60, 180), (120, 100), (180, 180))),
TestGeom('LINESTRING (0 0, 5 5, 10 5, 10 10)', n_p=4, centroid=(6.1611652351681556, 4.6966991411008934),
         tup=((0, 0), (5, 5), (10, 5), (10, 10)), ),
)

# Linear Rings
linearrings = (TestGeom(
    'LINEARRING (649899.3065171393100172 4176512.3807915160432458, 649902.7294133581453934 4176512.7834989596158266, 649906.5550170192727819 4176514.3942507002502680, 649910.5820134161040187 4176516.0050024418160319, 649914.4076170771149918 4176518.0184616246260703, 649917.2264131171396002 4176519.4278986593708396, 649920.0452871860470623 4176521.6427505780011415, 649922.0587463703704998 4176522.8507948759943247, 649924.2735982896992937 4176524.4616246484220028, 649926.2870574744883925 4176525.4683542405255139, 649927.8978092158213258 4176526.8777912775985897, 649929.3072462501004338 4176528.0858355751261115, 649930.1126611357321963 4176529.4952726080082357, 649927.4951798024121672 4176506.9444361114874482, 649899.3065171393100172 4176512.3807915160432458)',
    n_p=15),
)

# MultiLineStrings
multilinestrings = (TestGeom('MULTILINESTRING ((0 0, 0 100), (100 0, 100 100))', n_p=4, centroid=(50, 50),
                             tup=(((0, 0), (0, 100)), ((100, 0), (100, 100)))),
                    TestGeom(
                        'MULTILINESTRING ((20 20, 60 60), (20 -20, 60 -60), (-20 -20, -60 -60), (-20 20, -60 60), (-80 0, 0 80, 80 0, 0 -80, -80 0), (-40 20, -40 -20), (-20 40, 20 40), (40 20, 40 -20), (20 -40, -20 -40))',
                        n_p=21, centroid=(0, 0), tup=(
                        ((20., 20.), (60., 60.)), ((20., -20.), (60., -60.)), ((-20., -20.), (-60., -60.)),
                        ((-20., 20.), (-60., 60.)), ((-80., 0.), (0., 80.), (80., 0.), (0., -80.), (-80., 0.)),
                        ((-40., 20.), (-40., -20.)), ((-20., 40.), (20., 40.)), ((40., 20.), (40., -20.)),
                        ((20., -40.), (-20., -40.))))
)

# ====================================================
# Topology Operations

topology_geoms = ( (TestGeom('POLYGON ((-5.0 0.0, -5.0 10.0, 5.0 10.0, 5.0 0.0, -5.0 0.0))'),
                    TestGeom('POLYGON ((0.0 -5.0, 0.0 5.0, 10.0 5.0, 10.0 -5.0, 0.0 -5.0))')
                   ),
                   (TestGeom('POLYGON ((2 0, 18 0, 18 15, 2 15, 2 0))'),
                    TestGeom(
                        'POLYGON ((10 1, 11 3, 13 4, 15 6, 16 8, 16 10, 15 12, 13 13, 11 12, 10 10, 9 12, 7 13, 5 12, 4 10, 4 8, 5 6, 7 4, 9 3, 10 1))'),
                   ),
)

intersect_geoms = ( TestGeom('POLYGON ((5 5,5 0,0 0,0 5,5 5))'),
                    TestGeom(
                        'POLYGON ((10 1, 9 3, 7 4, 5 6, 4 8, 4 10, 5 12, 7 13, 9 12, 10 10, 11 12, 13 13, 15 12, 16 10, 16 8, 15 6, 13 4, 11 3, 10 1))'),
)

union_geoms = ( TestGeom('POLYGON ((-5 0,-5 10,5 10,5 5,10 5,10 -5,0 -5,0 0,-5 0))'),
                TestGeom('POLYGON ((2 0, 2 15, 18 15, 18 0, 2 0))'),
)

diff_geoms = ( TestGeom('POLYGON ((-5 0,-5 10,5 10,5 5,0 5,0 0,-5 0))'),
               TestGeom(
                   'POLYGON ((2 0, 2 15, 18 15, 18 0, 2 0), (10 1, 11 3, 13 4, 15 6, 16 8, 16 10, 15 12, 13 13, 11 12, 10 10, 9 12, 7 13, 5 12, 4 10, 4 8, 5 6, 7 4, 9 3, 10 1))'),
)

sdiff_geoms = ( TestGeom('MULTIPOLYGON (((-5 0,-5 10,5 10,5 5,0 5,0 0,-5 0)),((0 0,5 0,5 5,10 5,10 -5,0 -5,0 0)))'),
                TestGeom(
                    'POLYGON ((2 0, 2 15, 18 15, 18 0, 2 0), (10 1, 11 3, 13 4, 15 6, 16 8, 16 10, 15 12, 13 13, 11 12, 10 10, 9 12, 7 13, 5 12, 4 10, 4 8, 5 6, 7 4, 9 3, 10 1))'),
)

relate_geoms = ( (TestGeom('MULTIPOINT(80 70, 20 20, 200 170, 140 120)'),
                  TestGeom('MULTIPOINT(80 170, 140 120, 200 80, 80 70)'),
                  '0F0FFF0F2', True,),
                 (TestGeom('POINT(20 20)'), TestGeom('POINT(40 60)'),
                  'FF0FFF0F2', True,),
                 (TestGeom('POINT(110 110)'),
                  TestGeom('LINESTRING(200 200, 110 110, 200 20, 20 20, 110 110, 20 200, 200 200)'),
                  '0FFFFF1F2', True,),
                 (TestGeom('MULTILINESTRING((20 20, 90 20, 170 20), (90 20, 90 80, 90 140))'),
                  TestGeom('MULTILINESTRING((90 20, 170 100, 170 140), (130 140, 130 60, 90 20, 20 90, 90 20))'),
                  'FF10F0102', True,),
)

buffer_geoms = ( (TestGeom('POINT(0 0)'),
                  TestGeom(
                      'POLYGON ((5 0,4.903926402016153 -0.97545161008064,4.619397662556435 -1.913417161825447,4.157348061512728 -2.777851165098009,3.53553390593274 -3.535533905932735,2.777851165098015 -4.157348061512724,1.913417161825454 -4.619397662556431,0.975451610080648 -4.903926402016151,0.000000000000008 -5.0,-0.975451610080632 -4.903926402016154,-1.913417161825439 -4.619397662556437,-2.777851165098002 -4.157348061512732,-3.53553390593273 -3.535533905932746,-4.157348061512719 -2.777851165098022,-4.619397662556429 -1.913417161825462,-4.903926402016149 -0.975451610080656,-5.0 -0.000000000000016,-4.903926402016156 0.975451610080624,-4.619397662556441 1.913417161825432,-4.157348061512737 2.777851165097995,-3.535533905932752 3.535533905932723,-2.777851165098029 4.157348061512714,-1.913417161825468 4.619397662556426,-0.975451610080661 4.903926402016149,-0.000000000000019 5.0,0.975451610080624 4.903926402016156,1.913417161825434 4.61939766255644,2.777851165097998 4.157348061512735,3.535533905932727 3.535533905932748,4.157348061512719 2.777851165098022,4.619397662556429 1.91341716182546,4.90392640201615 0.975451610080652,5 0))'),
                  5.0, 8),
                 (TestGeom('POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))'),
                  TestGeom(
                      'POLYGON ((-2 0,-2 10,-1.961570560806461 10.390180644032258,-1.847759065022573 10.765366864730179,-1.662939224605091 11.111140466039204,-1.414213562373095 11.414213562373096,-1.111140466039204 11.662939224605092,-0.765366864730179 11.847759065022574,-0.390180644032256 11.961570560806461,0 12,10 12,10.390180644032256 11.961570560806461,10.765366864730179 11.847759065022574,11.111140466039204 11.66293922460509,11.414213562373096 11.414213562373096,11.66293922460509 11.111140466039204,11.847759065022574 10.765366864730179,11.961570560806461 10.390180644032256,12 10,12 0,11.961570560806461 -0.390180644032256,11.847759065022574 -0.76536686473018,11.66293922460509 -1.111140466039204,11.414213562373096 -1.414213562373095,11.111140466039204 -1.66293922460509,10.765366864730179 -1.847759065022573,10.390180644032256 -1.961570560806461,10 -2,0.0 -2.0,-0.390180644032255 -1.961570560806461,-0.765366864730177 -1.847759065022575,-1.1111404660392 -1.662939224605093,-1.41421356237309 -1.4142135623731,-1.662939224605086 -1.111140466039211,-1.84775906502257 -0.765366864730189,-1.961570560806459 -0.390180644032268,-2 0))'),
                  2.0, 8),
)

json_geoms = (TestGeom('POINT(100 0)', json='{ "type": "Point", "coordinates": [ 100.000000, 0.000000 ] }'),
              TestGeom('POLYGON((0 0, -10 0, -10 -10, 0 -10, 0 0))',
                       json='{ "type": "Polygon", "coordinates": [ [ [ 0.000000, 0.000000 ], [ -10.000000, 0.000000 ], [ -10.000000, -10.000000 ], [ 0.000000, -10.000000 ], [ 0.000000, 0.000000 ] ] ] }'),
              TestGeom(
                  'MULTIPOLYGON(((102 2, 103 2, 103 3, 102 3, 102 2)), ((100.0 0.0, 101.0 0.0, 101.0 1.0, 100.0 1.0, 100.0 0.0), (100.2 0.2, 100.8 0.2, 100.8 0.8, 100.2 0.8, 100.2 0.2)))',
                  json='{ "type": "MultiPolygon", "coordinates": [ [ [ [ 102.000000, 2.000000 ], [ 103.000000, 2.000000 ], [ 103.000000, 3.000000 ], [ 102.000000, 3.000000 ], [ 102.000000, 2.000000 ] ] ], [ [ [ 100.000000, 0.000000 ], [ 101.000000, 0.000000 ], [ 101.000000, 1.000000 ], [ 100.000000, 1.000000 ], [ 100.000000, 0.000000 ] ], [ [ 100.200000, 0.200000 ], [ 100.800000, 0.200000 ], [ 100.800000, 0.800000 ], [ 100.200000, 0.800000 ], [ 100.200000, 0.200000 ] ] ] ] }'),
              TestGeom('GEOMETRYCOLLECTION(POINT(100 0),LINESTRING(101.0 0.0, 102.0 1.0))',
                       json='{ "type": "GeometryCollection", "geometries": [ { "type": "Point", "coordinates": [ 100.000000, 0.000000 ] }, { "type": "LineString", "coordinates": [ [ 101.000000, 0.000000 ], [ 102.000000, 1.000000 ] ] } ] }',
              ),
              TestGeom('MULTILINESTRING((100.0 0.0, 101.0 1.0),(102.0 2.0, 103.0 3.0))',
                       json="""

{ "type": "MultiLineString",
  "coordinates": [
      [ [100.0, 0.0], [101.0, 1.0] ],
      [ [102.0, 2.0], [103.0, 3.0] ]
    ]
  }

""",
                       not_equal=True,
              ),
)

# For testing HEX(EWKB).
ogc_hex = '01010000000000000000000000000000000000F03F'
# `SELECT ST_AsHEXEWKB(ST_GeomFromText('POINT(0 1)', 4326));`
hexewkb_2d = '0101000020E61000000000000000000000000000000000F03F'
# `SELECT ST_AsHEXEWKB(ST_GeomFromEWKT('SRID=4326;POINT(0 1 2)'));`
hexewkb_3d = '01010000A0E61000000000000000000000000000000000F03F0000000000000040'
