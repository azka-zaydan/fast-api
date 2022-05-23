import mysql.connector

data = {
    "host": "localhost",
    "port": "6033",
    "user": "root",
    "password": "1234"

}

try:
    db_conn = mysql.connector.connect(**data)
    print("OK")
except:
    print("Error")