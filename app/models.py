from database import Base
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
class Post(Base):
    __tablename__ =  "posts"

    id = Column(Integer,primary_key = True,nullable = False)
    title = Column(String(1000),nullable = False)
    content = Column(String(1000),nullable = False)
    published = Column(Boolean,server_default = "1",nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False, server_default=text('now()'))