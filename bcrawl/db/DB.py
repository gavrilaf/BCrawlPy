from datetime import date
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Provider(object):
    YANDEX = 'yandex'
    TWITTER = 'twitter'


class Query(Base):
    __tablename__ = 'Queries'
    id = Column(Integer, primary_key=True)
    provider = Column(String)
    text = Column(String)
    start_from = Column(Date)

    day_queries = relationship("DayQuery", backref=backref('query', order_by='DayQuery.day'))
 
    def __init__(self, provider, text, start_from):
        self.provider = provider
        self.text = text
        self.start_from = start_from
    
    def __repr__(self):
        return ("<Query('%s','%s', '%s')>" % (self.provider, self.text, str(self.start_from))).encode('utf-8')


class DayQuery(Base):
    STATUS_NEW = 1
    STATUS_IN_PROGRESS = 2
    STATUS_COMPLETED = 3

    __tablename__ = 'DayQueries'
    id = Column(Integer, primary_key=True)
    query_id = Column(Integer, ForeignKey('Queries.id'))
    day = Column(Date)
    status = Column(Integer)

    def __repr__(self):
        return ("<DayQuery(%s, '%s','%s', '%s')>" % (self.id, self.query_id, str(self.day), self.status)).encode('utf-8')
        