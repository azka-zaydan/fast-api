#! /usr/bin/python
import os
import time
time.sleep(3)
os.system('docker exec -it db-fast-api_fast-api-db_1 mysql -u root -p')