go2mrrc
=======

## Simple Version ##

Each GO term is associated with many MMRRC strains. To see a brief report use
the following command.

```
python3 go2mmrrc.py mmrrc_catalog_data.csv.gz mgi_header.tsv.gz
```

If you want to see everything in JSON, do this.

```
python3 go2mmrrc.py mmrrc_catalog_data.csv.gz mgi_header.tsv.gz --json
```

## Persistent Version ##

Build test database (reads only 5k records from each file).

```
python3 gommsql.py create --mmrrc mmrrc_catalog_data.csv.gz --mgi mgi_header.tsv.gz --testing
```

Query database with a couple GO identifiers. Writes JSON to stdout.

```
python3 gommsql.py query GO:0005102 GO:0006654
```

Complete build. Takes a minute to run. Uses ~300M in filesystem.

```
rm g2m.db
python3 gommsql.py create --mmrrc mmrrc_catalog_data.csv.gz --mgi mgi_header.tsv.gz
python3 gommsql.py query GO:0000036 GO:0019202
```

## Dynamic Webpage ##

One-time setup to get python Flask.

```
conda env create -f env.yml
```

Some enviroment variables need to be set.

```
sh setup.sh
```

Run the web application.

```
fask run
```

Navigate web browser to http://127.0.0.1:5000 to see the dynamic demo app.
