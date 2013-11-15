import datetime
import copy
from pymongo import MongoClient

class PostInfo(object):
	def __init__(self, p):
		self.link = p.link
		self.publish_date = p.publish_date

		self.queries = []

class Repository(object):

	def __init__(self, db_name = 'bcrawl', collection_name = 'dub_filter'):
		self.client = MongoClient()
		self.db = self.client[db_name]
		self.collection = self.db[collection_name]

	def close(self):
		self.client.close()

	def clear_table_table(self):
		self.collection.remove()

	def find_post(self, link):
		'''If post found returns PostInfo object, else returns None'''
		self.collection.find_one({'link' : link})

	def store_post_info(self, info):
		self.collection.insert(info)