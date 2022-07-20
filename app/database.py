from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

pymysql.install_as_MySQLdb()

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:1234@localhost:3306/fastdbnew'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db_conn():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
