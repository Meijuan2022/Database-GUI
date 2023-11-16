# This file will creat a class to map with database file
# __________________________________ #

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from  sqlalchemy.orm import sessionmaker
from  sqlalchemy import or_

#use mysql
# import pymysql
# pymysql.install_as_MySQLdb()

#use sqlite
import sqlite3

# config using sqlite

import sqlite3

configuration = 'sqlite:///Members.db'
engine = create_engine(configuration, echo = True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Create class which would map to database
class Medlemmar(Base):
    __tablename__ = 'medlemmar'
    #__table_args__ ={'mysql_engine':'InnoDB'}
    MedlNr = Column(Integer,primary_key = True)
    Firstname = Column(String(20))
    Eftername = Column(String(20))
    Gatuadress =Column(String(20))
    PostNr = Column(Integer)
    PostAdress = Column(String(20))
    Fee = Column(Integer)
    def __init__(self,FN,EN,GA,PN,PA,F):
        self.Firstname =FN
        self.Eftername = EN
        self.Gatuadress = GA
        self.PostNr = PN
        self.PostAdress = PA
        self.Fee = F

def CreatDb ():
    Base.metadata.create_all(engine)



if __name__ == '__main__':
    CreatDb()
