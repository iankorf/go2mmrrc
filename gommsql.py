import argparse
import csv
import gzip
import json
import os
import random
import re
import sqlite3
import sys

def table_reader(file, delim, kidx, vidx, testing):
	data = {}
	counter = 0
	with gzip.open(file, 'rt') as fp:
		header = next(fp)
		reader = csv.reader(fp, delimiter=delim)
		for row in reader:
			counter += 1
			if testing and counter > 5000: break
			key = row[kidx]
			val = row[vidx]
			if val == '': continue
			if key not in data: data[key] = set()
			data[key].add(val)
	return data

def create_database(arg):
	if os.path.exists(arg.database): sys.exit('database already exists')
	mgi2mmrrc = table_reader(arg.mmrrc, ',', 10, 0, arg.testing)
	go2mgi = table_reader(arg.mgi, '\t', 4, 1, arg.testing)

	con = sqlite3.connect(arg.database)
	cur = con.cursor()
	cur.execute('CREATE TABLE go2mm(goid, mmid)')
	con.commit()

	go2mmrrc = {}
	for go_id, mgi_ids in go2mgi.items():
		if not go_id.startswith('GO'): continue
		for mgi_id in mgi_ids:
			if not re.match(r'^MGI:\d+$', mgi_id): continue
			if mgi_id not in mgi2mmrrc: continue
			for mmrrc_id in mgi2mmrrc[mgi_id]:
				if go_id not in go2mmrrc: go2mmrrc[go_id] = []
				go2mmrrc[go_id].append(mmrrc_id)

	for goid, mmids in go2mmrrc.items():
		for mmid in mmids:
			cur.execute(f'INSERT INTO go2mm VALUES("{goid}","{mmid}")')
	con.commit()

def query_database(arg):
	con = sqlite3.connect(arg.database)
	cur = con.cursor()
	result = {}
	for id in arg.goids:
		r = cur.execute(f'SELECT mmid from go2mm WHERE goid="{id}"').fetchall()
		con.commit()
		mids = [x[0] for x in r]
		result[id] = mids
	print(json.dumps(result, indent=2))

#########
## CLI ##
#########

parser = argparse.ArgumentParser(description='GO to MMRRC database utility')
sub = parser.add_subparsers(required=True, help='sub-commands')

## create sub-command ##
sub1 = sub.add_parser('create', help='make database')
sub1.add_argument('--mmrrc', required=True, metavar='<file.csv.gz>',
	help='mmrrc csv dump')
sub1.add_argument('--mgi', required=True, metavar='<file.tsv.gz>',
	help='mgi tsv dump')
sub1.add_argument('--database', required=False, metavar='<file.db>',
	default='g2m.db', help='database [%(default)s]')
sub1.add_argument('--testing', action='store_true')
sub1.set_defaults(func=create_database)

## query sub-command ##
sub2 = sub.add_parser('query', help='query database')
sub2.add_argument('goids', nargs='+', metavar='<GO:ID>',
	help='GO identifiers')
sub2.add_argument('--database', required=False, metavar='<file.db>',
	default='g2m.db', help='database [%(default)s]')
sub2.set_defaults(func=query_database)

## finish up ##
arg = parser.parse_args()
arg.func(arg)
