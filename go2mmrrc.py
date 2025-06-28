import argparse
import csv
import gzip
import json

def table_reader(file, delim, kidx, vidx):
	data = {}
	with gzip.open(file, 'rt') as fp:
		header = next(fp)
		reader = csv.reader(fp, delimiter=delim)
		for row in reader:
			key = row[kidx]
			val = row[vidx]
			if val == '': continue
			if key not in data: data[key] = set()
			data[key].add(val)
	return data

parser = argparse.ArgumentParser()
parser.add_argument('mmrrc', help='mmrrc catalog csv')
parser.add_argument('mgi', help='mgi tsv')
parser.add_argument('--json', action='store_true')
arg = parser.parse_args()

mgi2mmrrc = table_reader(arg.mmrrc, ',', 10, 0)
go2mgi = table_reader(arg.mgi, '\t', 4, 1)

go2mmrrc = {}
for go_id, mgi_ids in go2mgi.items():
	if not go_id.startswith('GO'): continue
	for mgi_id in mgi_ids:
		if mgi_id not in mgi2mmrrc: continue
		for mmrrc_id in mgi2mmrrc[mgi_id]:
			if go_id not in go2mmrrc: go2mmrrc[go_id] = []
			go2mmrrc[go_id].append(mmrrc_id)

if arg.json:
	print(json.dumps(go2mmrrc, indent=2))
else:
	for go_id, mmrrc_ids in go2mmrrc.items(): print(go_id, len(mmrrc_ids))
