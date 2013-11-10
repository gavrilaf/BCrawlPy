from bcrawl.base.MQData import MonitorMsg
from pymongo import MongoClient

class Repository(object):
	ALL = 1
	HOUR = 2
	DAY = 3

	def __init__(self, db_name = 'bcrawl', collection_name = 'monitor'):
		self.client = MongoClient()
		self.db = self.client[db_name]
		self.collection = self.db[collection_name]

		self.queries = {'yandex_search' : 		{'type': MonitorMsg.HTTP_SEARCH_YANDEX, 	'status' : MonitorMsg.OK},
						'yandex_content' : 		{'type': MonitorMsg.HTTP_CONTENT_YANDEX, 	'status' : MonitorMsg.OK},
						'lj_content' : 			{'type': MonitorMsg.HTTP_CONTENT_LJ, 		'status' : MonitorMsg.OK},
						'vk_content' : 			{'type': MonitorMsg.HTTP_CONTENT_VK, 		'status' : MonitorMsg.OK},
						'yandex_search_err' : 	{'type': MonitorMsg.HTTP_SEARCH_YANDEX, 	'status' : MonitorMsg.ERROR},
						'yandex_content_err' : 	{'type': MonitorMsg.HTTP_CONTENT_YANDEX, 	'status' : MonitorMsg.ERROR},
						'lj_content_err' : 		{'type': MonitorMsg.HTTP_CONTENT_LJ, 		'status' : MonitorMsg.ERROR},
						'vk_content_err' : 		{'type': MonitorMsg.HTTP_CONTENT_VK, 		'status' : MonitorMsg.ERROR},
						'queries_sent' : 		{'type': MonitorMsg.DAY_QUERY_SENT, 		'status' : MonitorMsg.OK},
						'queries_completed' : 	{'type': MonitorMsg.DAY_QUERY_COMPLETED, 	'status' : MonitorMsg.OK}}

	def close(self):
		self.client.close()

	def clear_monitor_table(self):
		self.collection.remove()

	def store_msg(self, msg):
		self.collection.insert(msg.mongo_rep())

	def get_query(self, name, scope):
		return self.queries[name]

	def yandex_search_requests(self, scope = ALL):
		return self.collection.find(self.get_query('yandex_search', scope)).count()
		
	def yandex_content_requests(self, scope = ALL):
		return self.collection.find(self.get_query('yandex_content', scope)).count()

	def lj_content_requests(self, scope = ALL):
		return self.collection.find(self.get_query('lj_content', scope)).count()

	def vk_content_requests(self, scope = ALL):
		return self.collection.find(self.get_query('vk_content', scope)).count()

	def queries_sent(self, scope = ALL):
		return self.collection.find(self.get_query('queries_sent', scope)).count()

	def queries_completed(self, scope = ALL):
		return self.collection.find(self.get_query('queries_completed', scope)).count()

	