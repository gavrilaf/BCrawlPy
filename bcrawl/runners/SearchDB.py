#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from bcrawl.base import DB


class SObject(DB.Base):
    __tablename__ = 'SObjects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    queries = relationship('Query')

    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return ('<SObject(%d, %s)>' % (self.id, self.name))
   

class Query(DB.Base):
    __tablename__ = 'Queries'

    id = Column(Integer, primary_key=True)
    provider = Column(Integer)
    text = Column(String)
    start_from = Column(Date)
    sobject_id = Column(Integer, ForeignKey('SObjects.id'))

    day_queries = relationship('DayQuery', order_by='DayQuery.day')
    posts = relationship('Post')
    
    def __init__(self, sobj_id, provider, text, start_from):
        self.sobject_id = sobj_id
        self.provider = provider
        self.text = text
        self.start_from = start_from
    
    def __repr__(self):
        return ('<Query(%d, %s, %s, %s)>' % 
            (self.id, self.provider, self.text, self.start_from))


class DayQuery(DB.Base):
    __tablename__ = 'DayQueries'

    STATUS_NEW = 1
    STATUS_IN_PROGRESS = 2
    STATUS_COMPLETED = 3
    
    id = Column(Integer, primary_key=True)
    query_id = Column(Integer, ForeignKey('Queries.id'))
    day = Column(Date)
    status = Column(Integer)

    def __init__(self, query_id, day, status):
        self.query_id = query_id
        self.day = day
        self.status = status

    def __repr__(self):
        return ('<DayQuery(%d, %d, %s, %d)>' % 
            (self.id, self.query_id, self.day, self.status))


class Post(DB.Base):
    __tablename__ = 'Posts'

    id = Column(Integer, primary_key=True)
    
    title = Column(String)
    link = Column(String)
    publish_date = Column(DateTime)
    collected_date = Column(DateTime)
    
    query_id = Column(Integer, ForeignKey('Queries.id'))
    author_id = Column(Integer, ForeignKey('Authors.id'))
    blog_host_id = Column(Integer, ForeignKey('BlogHosts.id'))

    content = relationship('PostContent', uselist=False, backref='post')

class Author(DB.Base):
    __tablename__ = 'Authors'

    id = Column(Integer, primary_key=True)
    blog = Column(String)

    posts = relationship('Post')

class BlogHost(DB.Base):
    __tablename__ = 'BlogHosts'

    id = Column(Integer, primary_key=True)
    host = Column(String)    

    posts = relationship('Post')

class PostContent(DB.Base):
    __tablename__ = 'PostContents'

    id = Column(Integer, primary_key=True)
    content = Column(String)

    post_id = Column(Integer, ForeignKey('Posts.id'))