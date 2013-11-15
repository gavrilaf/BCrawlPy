import datetime
import copy
from pymongo import MongoClient

class PostInfo(object):

	@staticmethod
	def from_mongo(json) :
		pi = PostInfo()
		pi.id = json['_id']
		pi.link = json['link']
		pi.publish_date = json['publish_date']
		pi.queries = json['queries']

		return pi

	def __init__(self):
		self.id = None
		self.link = ''
		self.publish_date = None
		self.queries = []

	def mongo_rep(self):
		obj = {'link' : self.link, 'publish_date' : self.publish_date, 'queries' : self.queries}
		if self.id is not None:
			obj['_id'] = self.id
		return obj

	def __str__(self):
		return str(self.mongo_rep())

class Repository(object):

	def __init__(self, db_name = 'bcrawl', collection_name = 'dub_filter'):
		self.client = MongoClient()
		self.db = self.client[db_name]
		self.collection = self.db[collection_name]

	def close(self):
		self.client.close()

	def clear_table(self):
		self.collection.remove()

	def find_pinfo(self, link):
		'''If post found returns PostInfo object, else returns None'''
		p = self.collection.find_one({'link' : link})
		if p is None:
			return None

		return PostInfo.from_mongo(p)

	def store_pinfo(self, info):
		self.collection.save(info.mongo_rep())