from pymongo import MongoClient

class Repository(object):

	def __init__(self):
		self.client = MongoClient()
		self.db = self.client['bcrawl']
		self.collection = self.db['monitor']

	def close(self):
		self.client.close()

	def store_msg(self, msg):
		self.collection.insert(msg.mongo_rep())

	def yandex_search_requests_count(self):
		return self.collection.find({"type": 1}).count()
		
	def yandex_content_requests_count(self):
		return self.collection.find({"type": 2}).count()

	def lj_content_requests_count(self):
		return self.collection.find({"type": 3}).count()

	def vk_content_requests_count(self):
		return self.collection.find({"type": 4}).count()

	def queries_fired(self):
		return 0

	def queries_completed_count(self):
		return self.collection.find({"type": 6}).count()

	def posts_found_count(self):
		return 0

	def post_dublicates_count(self):
		return 0
		
	def posts_filtered_count(self):
		return self.collection.find({"type": 5}).count()

	def posts_persisted_count(self):
		return self.collection.find({"type": 7}).count()
