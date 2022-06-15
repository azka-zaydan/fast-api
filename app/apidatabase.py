from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

pymysql.install_as_MySQLdb()

sqlalchemy_database_url = 'mysql://root:1234@localhost:6033/fastdb'

engine = create_engine(sqlalchemy_database_url)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db_conn():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
