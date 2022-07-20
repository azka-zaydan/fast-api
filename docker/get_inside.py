#! /usr/bin/python
import os
import time
time.sleep(3)
os.system('docker exec -i -t fast-api-db mysql -u root -p')
