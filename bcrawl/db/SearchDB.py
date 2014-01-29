#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from dateutil.rrule import *
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
import DB


class SObject(DB.Base):
    __tablename__ = 'SObjects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    queries = relationship('Query')

    def __init__(self, name):
        self.name = name

    def __unicode__(self):
        return u"SObject(%d, %s)" % (self.id, self.name)
        
class Query(DB.Base):
    __tablename__ = 'Queries'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    start_from = Column(Date)
    sobject_id = Column(Integer, ForeignKey('SObjects.id'), nullable = False)

    day_queries = relationship('DayQuery', backref = backref('query', order_by='DayQuery.day'))
    posts = relationship('Post')
    
    def __init__(self, sobj_id, text, start_from):
        self.sobject_id = sobj_id
        self.text = text
        self.start_from = start_from


    def get_days_to_now(self):
        if self.day_queries:
            start = self.day_queries[-1].day
            remove_first = True
        else:
            start = self.start_from
            remove_first = False

        days = []

        lst = list(rrule(DAILY, dtstart = start, until = datetime.datetime.now()))
        if remove_first:
            del lst[0]
        
        for dt in lst:
            days.append(dt.date())

        return days
        
    def __unicode__(self):
        return u"Query(%d, %d, %s, %s)" % (self.id, self.sobject_id, self.text, self.start_from)

class DayQuery(DB.Base):
    __tablename__ = 'DayQueries'

    STATUS_NEW = 1
    STATUS_IN_PROGRESS = 2
    STATUS_COMPLETED = 3
    
    id = Column(Integer, primary_key=True)
    query_id = Column(Integer, ForeignKey('Queries.id'), nullable = False)
    day = Column(Date)
    status = Column(Integer)

    def __init__(self, query_id, day, status):
        self.query_id = query_id
        self.day = day
        self.status = status

    def __unicode__(self):
        return u"DayQuery(%d, %d, %s, %d)" % (self.id, self.query_id, self.day, self.status)


class Post(DB.Base):
    __tablename__ = 'Posts'

    id = Column(Integer, primary_key=True)
    
    title = Column(String)
    link = Column(String)
    publish_date = Column(DateTime)
    collected_date = Column(DateTime)
    
    query_id = Column(Integer, ForeignKey('Queries.id'), nullable = False)
    author_id = Column(Integer, ForeignKey('Authors.id'), nullable = False)
    blog_host_id = Column(Integer, ForeignKey('BlogHosts.id'), nullable = False)

    content = relationship('PostContent', uselist=False, backref='post')

    def __unicode__(self):
        return u"Post(%d, %s, %s, %s, %s, %s, %s, %s)" % (self.id, self.title, self.link, self.publish_date, self.collected_date, self.query_id, self.author_id, self.blog_host_id)

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

    post_id = Column(Integer, ForeignKey('Posts.id'), nullable = False)