REGION_LIST_QUERY = """
	SELECT region.name, substring(district.name FROM 7)
	FROM planet_osm_line AS region 
	JOIN planet_osm_line AS district 
	ON region.ref = substring(district.ref FROM 0 for 6)
	WHERE region.name LIKE '%kraj' 
	AND district.name LIKE 'okres%'
	AND region.admin_level = '4' 
	AND district.admin_level = '8'
	GROUP BY region.name, district.name
	ORDER BY region.name, district.name
"""

SHOW_ALL_QUERY = """
	SELECT amenity, ST_ASGEOJSON(way)
	FROM planet_osm_point 
	WHERE amenity IN ('hospital', 'pharmacy')
"""