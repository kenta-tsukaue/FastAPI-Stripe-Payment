from sqlalchemy import create_engine
import sys
from sqlalchemy.orm import (sessionmaker, relationship, scoped_session)

sys.dont_write_bytecode = True

#setting db connection
url = "mysql+pymysql://root:[your_password]@localhost:3306/[database_name]?charset=utf8"
engine = create_engine(url, echo=False, pool_recycle=10)

#create session
def create_new_session():
    return  scoped_session(sessionmaker(autocommit=False, autoflush=True, expire_on_commit=False, bind=engine))