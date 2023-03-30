# Bridgecrew to Prisma Cloud Code Security migration automation.

## Python script for exporting data from Bridgecrew
* `bc-export.py` Requires BC_API_KEY

## Python script for importing data into Prisma Cloud Code Security
* `ccs-import.py` Requires PRISMA_API_URL, PRISMA_ACCESS_KEY_ID, PRISMA_SECRET_KEY

## Preparation for the very first run

```
git clone https://github.com/jneytchev-at-panw/bc-ccs-migration
cd bc-ccs-migration
mkdir data
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export BC_API_KEY=<your value>
python3 bc-export.py
tar zcvf data.tar.gz data/
deactivate
```

## Consecutive runs

```
cd bc-ccs-migration
git pull
# make sure the data directory exists
# activate venv if it is not already active

export BC_API_KEY=<your value>
python3 bc-export.py
tar zcvf data.tar.gz data/
deactivate
```



