from settings import DB_AMENITY_TYPES

DISTRICT_LIST_QUERY = """
	SELECT region.name, district.name, ST_ASGEOJSON(district.way)
	FROM planet_osm_line AS region 
	JOIN planet_osm_line AS district 
	ON region.ref = substring(district.ref FROM 0 for 6)
	WHERE region.admin_level = '4' 
	AND district.admin_level = '8'
	ORDER BY region.name, district.name
"""

"""
Query that finds all objects by amenity
"""
SHOW_ALL_QUERY = """
	SELECT amenity AS type, ST_ASGEOJSON(way), name
	FROM planet_osm_point 
	WHERE amenity IN ('{}')
""".format('\',\''.join(DB_AMENITY_TYPES))

"""
Query that finds all objects by amenity in specific district
* district - replacement tag for district in http request 
"""
SHOW_BY_DISTRICT_QUERY = SHOW_ALL_QUERY + """
	AND ST_WITHIN(way,
	    (SELECT way
		FROM planet_osm_polygon
		WHERE name = district))
"""

"""
Query that finds all objects by amenity in distance of input coordinates
* lat, lng - replacement tags for latitude and longitude in http request 
* dist - replacement tag for distance in http request
"""
SHOW_BY_COORDS_QUERY = SHOW_ALL_QUERY + """
	AND ST_Distance(way, 
		(SELECT ST_GeomFromText('POINT(lng lat)', 4326))) < dist
"""