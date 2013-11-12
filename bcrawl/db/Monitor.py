import datetime
from bcrawl.base.MQData import MonitorMsg
from pymongo import MongoClient

class Repository(object):
	ALL = 1
	HOUR = 2
	DAY = 3

	POST_COLLECTED = 7
	POST_DUBLICATE_DETECTED = 8
	POST_UPDATE_DETECTED = 9
	POST_NEW_LINK_DETECTED = 10
	POST_SPAM_DETECTED = 11
	
	POST_PERSISTED = 12

	def __init__(self, db_name = 'bcrawl', collection_name = 'monitor'):
		self.client = MongoClient()
		self.db = self.client[db_name]
		self.collection = self.db[collection_name]

		self.queries = {'yandex_search' : 		{'type' : MonitorMsg.HTTP_SEARCH_YANDEX},
						'yandex_content' : 		{'type' : MonitorMsg.HTTP_CONTENT_YANDEX},
						'lj_content' : 			{'type' : MonitorMsg.HTTP_CONTENT_LJ},
						'vk_content' : 			{'type' : MonitorMsg.HTTP_CONTENT_VK},
						'queries_sent' : 		{'type' : MonitorMsg.QUERY_SENT},
						'queries_completed' : 	{'type' : MonitorMsg.QUERY_COMPLETED},
						'posts_collected' :		{'type' : MonitorMsg.POST_COLLECTED},
						'posts_dublicate' :		{'type' : MonitorMsg.POST_DUBLICATE_DETECTED},
						'posts_update' :		{'type' : MonitorMsg.POST_UPDATE_DETECTED},
						'posts_new_link' :		{'type' : MonitorMsg.POST_NEW_LINK_DETECTED},
						'posts_spam' :			{'type' : MonitorMsg.POST_SPAM_DETECTED},
						'posts_persisted' :		{'type' : MonitorMsg.POST_PERSISTED}}

	def close(self):
		self.client.close()

	def clear_monitor_table(self):
		self.collection.remove()

	def store_msg(self, msg):
		self.collection.insert(msg.mongo_rep())

	def get_query(self, name, success, scope):
		query = self.queries[name]
		if success:
			query['status'] = MonitorMsg.OK
		else:
			query['status'] = MonitorMsg.ERROR

		if scope == Repository.DAY:
			t = datetime.datetime.utcnow() - datetime.timedelta(days = 1)
			query.update({"timestamp": {"$gte": t}})
		elif scope == Repository.HOUR:
			t = datetime.datetime.utcnow() - datetime.timedelta(hours = 1)
			query.update({"timestamp": {"$gte": t}})
		
		return self.queries[name]

	def yandex_search_requests(self, scope = ALL):
		return self.collection.find(self.get_query('yandex_search', True, scope)).count()
		
	def yandex_content_requests(self, scope = ALL):
		return self.collection.find(self.get_query('yandex_content', True, scope)).count()

	def lj_content_requests(self, scope = ALL):
		return self.collection.find(self.get_query('lj_content', True, scope)).count()

	def vk_content_requests(self, scope = ALL):
		return self.collection.find(self.get_query('vk_content', True, scope)).count()

	def yandex_search_errors(self, scope = ALL):
		return self.collection.find(self.get_query('yandex_search', False, scope)).count()
		
	def yandex_content_errors(self, scope = ALL):
		return self.collection.find(self.get_query('yandex_content', False, scope)).count()

	def lj_content_errors(self, scope = ALL):
		return self.collection.find(self.get_query('lj_content', False, scope)).count()

	def vk_content_errors(self, scope = ALL):
		return self.collection.find(self.get_query('vk_content', False, scope)).count()


	def queries_sent(self, scope = ALL):
		return self.collection.find(self.get_query('queries_sent', True, scope)).count()

	def queries_completed(self, scope = ALL):
		return self.collection.find(self.get_query('queries_completed', True, scope)).count()

	
	def posts_collected(self, scope = ALL):
		return self.collection.find(self.get_query('posts_collected', True, scope)).count()

	def posts_update_detected(self, scope = ALL):
		return self.collection.find(self.get_query('posts_update', True, scope)).count()

	def posts_dublicate_detected(self, scope = ALL):
		return self.collection.find(self.get_query('posts_dublicate', True, scope)).count()

	def posts_new_link_detected(self, scope = ALL):
		return self.collection.find(self.get_query('posts_new_link', True, scope)).count()

	def posts_spam_detected(self, scope = ALL):
		return self.collection.find(self.get_query('posts_spam', True, scope)).count()

	def posts_persisted(self, scope = ALL):
		return self.collection.find(self.get_query('posts_persisted', True, scope)).count()



	