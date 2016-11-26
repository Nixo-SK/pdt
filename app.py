import json
import getpass
import psycopg2
import coord_parser
from flask import Flask, jsonify, request, send_from_directory
from queries import *
from settings import *


app = Flask(__name__)
app.debug = DEBUG

db = psycopg2.connect("host={} dbname={} user={} password={}".format(
	DB_HOST, DB_NAME, DB_USER, DB_PASS if DEBUG else getpass.getpass()))
cursor = db.cursor()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/icons', 'favicon.ico')
	
@app.route('/')
def index():
	return send_from_directory('', 'index.html')

@app.route('/available_types')
def available_types():
	return jsonify({'types': AMENITY_TYPES});

@app.route('/region_list')
def region_list():
	cursor.execute(REGION_LIST_QUERY)

	region_dict = {}
	for region in cursor.fetchall():
		district = {
			'name': region[1], 
			'coords': json.loads(region[2][35:-1])
		}

		if region[0] in region_dict:
			region_dict[region[0]].append(district)
		else:
			region_dict[region[0]] = [district]
	
	return jsonify([json.dumps({
		'region': k, 'districts': v}) for k, v in sorted(region_dict.items())])

@app.route('/show_all')
def show_all():	
	cursor.execute(SHOW_ALL_QUERY)
	return jsonify([
		json.dumps({
			'type': row[0], 
			'lng': json.loads(row[1])['coordinates'][0], 
			'lat': json.loads(row[1])['coordinates'][1]}) 
		for row in cursor.fetchall()])

if __name__ == '__main__':
	app.run()