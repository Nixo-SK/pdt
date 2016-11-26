from settings import AMENITY_TYPES

REGION_LIST_QUERY = """
	SELECT region.name, district.name, ST_ASGEOJSON(district.way)
	FROM planet_osm_line AS region 
	JOIN planet_osm_line AS district 
	ON region.ref = substring(district.ref FROM 0 for 6)
	WHERE region.admin_level = '4' 
	AND district.admin_level = '8'
	ORDER BY region.name, district.name
"""

DISTRICT_COORD_QUERY = """
	SELECT ST_ASGEOJSON(way)
"""

SHOW_ALL_QUERY = """
	SELECT amenity, ST_ASGEOJSON(way)
	FROM planet_osm_point 
	WHERE amenity IN ('{}')
""".format('\',\''.join(AMENITY_TYPES))