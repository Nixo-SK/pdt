import json
import getpass
import psycopg2
from flask import Flask, jsonify, request, send_from_directory
from queries import *

app = Flask(__name__)
#db = psycopg2.connect("host='localhost' dbname='postgres' user='postgres' password='{0}'".format(getpass.getpass()))
db = psycopg2.connect("host='localhost' dbname='postgres' user='postgres' password=rokogolf")
cursor = db.cursor()

def parse_regions(rows):
	region_dict = {}
	for row in rows:
		if row[0] in region_dict:
			region_dict[row[0]].append(row[1])
		else:
			region_dict[row[0]] = [row[1]]
	
	return [json.dumps({'region': k, 'districts': v}) for k, v in sorted(region_dict.items())]

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')
	
@app.route('/')
def index():
	return send_from_directory('', 'index.html')

@app.route('/region_list')
def regions():
	cursor.execute(REGION_LIST_QUERY)
	return jsonify(parse_regions(cursor.fetchall()))

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
	app.debug = True
	app.run()