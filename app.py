import json
import getpass
import psycopg2
from flask import Flask, jsonify, request, send_from_directory
from queries import *
from settings import *


app = Flask(__name__)
app.debug = DEBUG

db = psycopg2.connect("host={} dbname={} user={} password={}".format(
	DB_HOST, DB_NAME, DB_USER, DB_PASS if DEBUG else getpass.getpass()))
cursor = db.cursor()

def parse_result(rows):
	return jsonify([
		json.dumps({
			'type': row[0], 
			'lng': json.loads(row[1])['coordinates'][0], 
			'lat': json.loads(row[1])['coordinates'][1]}) 
		for row in rows])

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/icons', 'favicon.ico')
	
@app.route('/')
def index():
	return send_from_directory('', 'index.html')

@app.route('/available_types')
def available_types():
	return jsonify({'types': AMENITY_TYPES});

@app.route('/district_list')
def region_list():
	'''
	* finds all districts by region and parse their coordinates
	'''
	cursor.execute(DISTRICT_LIST_QUERY)
	district_dict = {}
	for row in cursor.fetchall():
		district = {
			'name': row[1], 
			'coords': json.loads(row[2][35:-1])
		}

		if row[0] in district_dict:
			district_dict[row[0]].append(district)
		else:
			district_dict[row[0]] = [district]
	
	return jsonify([
		json.dumps({
			'region': k, 
			'districts': v}) 
		for k, v in sorted(district_dict.items())])

@app.route('/show_all')
def show_all():	
	'''
	Scenario 1
	* shows all requested objects
	* objects can be filtered by type (amenity)
	'''
	cursor.execute(SHOW_ALL_QUERY)
	return parse_result(cursor.fetchall())

@app.route('/show_by_district')
def show_by_district():	
	'''
	Scenario 2
	* shows all requested objects that belong to distrinct parsed as a parameter
	* objects still can be filtered by type (amenity)
	'''
	cursor.execute(SHOW_BY_DISTRICT_QUERY.replace(
		'district', '\'' + request.args.get('district') + '\''))
	return parse_result(cursor.fetchall())

if __name__ == '__main__':
	app.run()