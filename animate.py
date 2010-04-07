import sys
import mapnik2
import cairo

prj = mapnik2.Projection("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
m = mapnik2.Map(1280, 768, prj.params())
m.background = mapnik2.Color('white')

district_lyr = mapnik2.Layer('Districts')
district_lyr.datasource = mapnik2.PostGIS(
    host='localhost', user='postgres', dbname='big_map',
    table="big_map_district")

district_style = mapnik2.Style()

all_rule = mapnik2.Rule()
all_rule.filter = mapnik2.Expression("[state_abbrev] != 'ak' and [state_abbrev] != 'hi' and [state_abbrev] != 'pr'")
all_rule.symbols.append(mapnik2.PolygonSymbolizer(mapnik2.Color('grey')))
district_style.rules.append(all_rule)

dem_rule = mapnik2.Rule()
dem_rule.filter = mapnik2.Expression("[party] = 'Democrat' and [state_abbrev] != 'ak' and [state_abbrev] != 'hi' and [state_abbrev] != 'pr'")

dem_rule.symbols.append(mapnik2.PolygonSymbolizer(mapnik2.Color(25, 58, 190)))

district_style.rules.append(dem_rule)

rep_rule = mapnik2.Rule()
rep_rule.filter = mapnik2.Expression("[party] = 'Republican' and [state_abbrev] != 'ak' and [state_abbrev] != 'hi' and [state_abbrev] != 'pr'")

rep_rule.symbols.append(mapnik2.PolygonSymbolizer(mapnik2.Color(163, 3, 3)))

district_style.rules.append(rep_rule)

border_rule = mapnik2.Rule()
border_rule.filter = mapnik2.Expression("[state_abbrev] != 'ak' and [state_abbrev] != 'hi' and [state_abbrev] != 'pr'")
lines = mapnik2.LineSymbolizer(mapnik2.Color('black'), 0.75*2)
lines.stroke.opacity = 0.5
lines.stroke.line_cap = mapnik2.line_cap.ROUND_CAP
lines.stroke.line_join = mapnik2.line_join.ROUND_JOIN
border_rule.symbols.append(lines)
district_style.rules.append(border_rule)

m.append_style('district', district_style)

district_lyr.styles.append('district')

m.layers.append(district_lyr)

ll_start = (-126.7332, 22.544, -64.9499, 51.3844)
ll_finish = (-73.967004000000102, 40.670499999999997, -73.860851000000096, 40.739339000000001)
ll = list(ll_start)

num_frames = 6000
z = 15
f = 1.0

for i in range(1, num_frames + 1):
    for j in range(0, 4):
        if i > 1:
            ll[j] = ll_finish[j] + ((ll[j]-ll_finish[j])*f)
            if f > 0.998:
                f = f - 0.00002

    c0 = prj.forward(mapnik2.Coord(ll[0], ll[1]))
    c1 = prj.forward(mapnik2.Coord(ll[2], ll[3]))
    bbox = mapnik2.Box2d(c0.x, c0.y, c1.x, c1.y)
    m.zoom_to_box(bbox)
    print "Rendering frame %d/%d" % (i, num_frames)
    mapnik2.render_to_file(m, 'frames/frame_%d.png' % i, 'png')
