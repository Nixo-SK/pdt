import sys
import json
import getpass
import psycopg2
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)
db = psycopg2.connect("host='localhost' dbname='postgres' user='postgres' password='{0}'".format(getpass.getpass()))
cursor = db.cursor()

def parse_JSON(obj):
	try:
		lng, lat = obj[1][16:-1].split()
		type = obj[0]
	except IndexError:
		lng, lat = obj[0][16:-1].split()
		type = 'global'
	finally:
		return json.dumps({'type': type, 'lng': lng, 'lat': lat})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')
	
@app.route('/')
def index():
	return send_from_directory('', 'index.html')		

@app.route('/query')
def query():	
	try:
		#lat = request.args.get('lat')
		#lng = request.args.get('lng')
		cursor.execute("select amenity, ST_AsEWKT(way) from planet_osm_point where amenity like 'hospital' or amenity like 'pharmacy'")
		# cursor.execute("select ST_AsEWKT(way) from planet_osm_point where amenity like 'hospital' or amenity like 'pharmacy'")
		return jsonify([parse_JSON(res) for res in cursor])
	except Exception as e:
		return jsonify(e)	
	
if __name__ == '__main__':
	app.debug = True
	app.run()