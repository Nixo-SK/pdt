import sys
import json
import getpass
import psycopg2
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)
db = psycopg2.connect("host='localhost' dbname='postgres' user='postgres' password='{0}'".format(getpass.getpass()))
cursor = db.cursor()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')
	
@app.route('/')
def index():
	return send_from_directory('', 'index.html')		

@app.route('/show_all')
def show_all():	
	cursor.execute("select amenity, ST_ASGEOJSON(way) from planet_osm_point where amenity in ('hospital', 'pharmacy')")
	return jsonify([json.dumps({'type': row[0], 'lng': json.loads(row[1])['coordinates'][0], 'lat': json.loads(row[1])['coordinates'][1]}) for row in cursor])

if __name__ == '__main__':
	app.debug = True
	app.run()