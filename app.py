import sys
import getpass
import psycopg2
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('./', 'index.html')		

if __name__ == '__main__':
	db = psycopg2.connect("host='localhost' dbname='postgres' user='postgres' password='{0}'".format(getpass.getpass()))
	app.debug = True
	app.run()