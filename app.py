import json
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
	con = sqlite3.connect('g2m.db')
	con.row_factory = sqlite3.Row
	return con


@app.route('/')
def index():
	records = []
	goids = 'GO:0005102', 'GO:0006654'
	con = get_db_connection()
	for x in goids:
		r = con.execute(f'SELECT mmid FROM go2mm WHERE goid="{x}"').fetchall()
		con.commit()
		mids = [x[0] for x in r]
		records.append({'GO': x, 'MMRRC': mids})
	return render_template('index.html', records=records)
