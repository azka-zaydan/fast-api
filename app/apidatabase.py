from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

pymysql.install_as_MySQLdb()

sqlalchemy_database_url = 'mysql+pymysql://root:1234@localhost:3306/fastdbnew'

engine = create_engine(sqlalchemy_database_url)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db_conn():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
