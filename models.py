# -*- encoding: utf-8 -*-
import datetime
import sys
from sqlalchemy import (Column, Integer, String, Text, ForeignKey,CHAR, VARCHAR, INT,  \
                create_engine, MetaData, DECIMAL, DATETIME, exc, event, Index, \
                and_)
from sqlalchemy.ext.declarative import declarative_base

sys.dont_write_bytecode = True

base = declarative_base()

class user(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    token = Column(String)