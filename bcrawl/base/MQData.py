#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime 
from dateutil import parser
import jsonpickle


class Post(object):

	NEW = 1
	UPDATED = 2
	NEW_LINK = 3
	DUBLICATE = 4

 	@staticmethod
	def from_values(query_id, provider, values_):
		'''
			Create new Post object from values array.
			Values contains [link, title, publish_date, author]

			Uses dateutil.parse for converting string date to datetime. 
		'''
		p = Post(query_id, provider, values_[0], values_[1], parser.parse(values_[2]), values_[3])
		p.cached_copy = values_[4]

		return p

	def __init__(self, query_id, provider, link, title, publish_date, author):
		self.query_id = query_id
		self.provider = provider
		self.title = title
		self.link = link
		self.publish_date = publish_date
		self.author = author
		self.host = None
		self.content = None

		self.collected = datetime.datetime.utcnow()
		self.status = Post.NEW

		self.cached_copy = '' # Only for Yandex

		self.content_error = False

	def __str__(self):
		s = '{%d, %s, %s, %s, %s, %s}' % (self.query_id, self.link, self.title, self.publish_date, self.author, self.host)

		return s

class DayQuery(object):
	def __init__(self, id_, query_id, text, day):
		self.id = id_
		self.query_id = query_id
		self.text = text
		self.day = day

	def __unicode__(self):
		return u'{%d, %d, %s, %s}' % (self.id, self.query_id, self.text, self.day)
		
class DayQueryStatus(object):
	OK = 1
	ERROR = 2

	def __init__(self, id_, status):
		self.id = id_
		self.status = status

	def __unicode__(self):
		return '{%d, %d}' % (self.id, self.status)

class MonitorMsg(object):
	QUERY_SENT = 1
	QUERY_COMPLETED = 2

	HTTP_SEARCH = 3
	HTTP_CONTENT = 4
	
	POST_COLLECTED = 5
	POST_DUBLICATE_DETECTED = 6
	POST_UPDATE_DETECTED = 7
	POST_NEW_LINK_DETECTED = 8
	POST_SPAM_DETECTED = 9
	
	POST_PERSISTED = 10

	OK = 1
	ERROR = 2
	
	def __init__(self, type_, provider, status, id_, text):
		self.type = type_
		self.provider = provider
		self.status = status
		self.id = id_
		self.text = text
		self.timestamp = datetime.datetime.utcnow()

	def __unicode__(self):
		return '{%d, %d, %d, %s, %s, %s}' % (self.type, self.provider, self.status, self.timestamp, self.id, self.text)

	def mongo_rep(self):
		obj = {
			'type' : self.type, 
			'provider' : self.provider, 
			'status' : self.status, 
			'timestamp' : self.timestamp, 
			'obj_id' : self.id, 
			'text' : self.text
		}

		return obj



