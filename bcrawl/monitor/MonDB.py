import datetime
import copy
from pymongo import MongoClient
from bcrawl.base.MQData import MonitorMsg

SCOPE_ALL = 1
SCOPE_HOUR = 2
SCOPE_DAY = 3

class Repository(object):
	""" 
		Interface to monitor database.
		Used from nonitor runner and monitor web.
	"""
	def __init__(self, db_name = 'bcrawl', collection_name = 'monitor'):
		self.client = MongoClient(tz_aware=True)
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

	def clear_table(self):
		self.collection.remove()

	def store_msg(self, msg):
		self.collection.insert(msg.mongo_rep())

	def get_query(self, name, success, scope):
		query = copy.deepcopy(self.queries[name])

		if success:
			query['status'] = MonitorMsg.OK
		else:
			query['status'] = MonitorMsg.ERROR

		if scope == SCOPE_DAY:
			t = datetime.datetime.utcnow() - datetime.timedelta(days = 1)
			query.update({"timestamp": {"$gte": t}})
		elif scope == SCOPE_HOUR:
			t = datetime.datetime.utcnow() - datetime.timedelta(hours = 1)
			query.update({"timestamp": {"$gte": t}})

		return query

	def yandex_search_requests(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('yandex_search', True, scope)).count()
		
	def yandex_content_requests(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('yandex_content', True, scope)).count()

	def lj_content_requests(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('lj_content', True, scope)).count()

	def vk_content_requests(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('vk_content', True, scope)).count()

	def yandex_search_errors(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('yandex_search', False, scope)).count()
		
	def yandex_content_errors(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('yandex_content', False, scope)).count()

	def lj_content_errors(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('lj_content', False, scope)).count()

	def vk_content_errors(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('vk_content', False, scope)).count()


	def queries_sent(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('queries_sent', True, scope)).count()

	def queries_completed(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('queries_completed', True, scope)).count()
	
	def queries_errors(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('queries_completed', False, scope)).count()

	
	def posts_collected(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('posts_collected', True, scope)).count()

	def posts_update_detected(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('posts_update', True, scope)).count()

	def posts_dublicate_detected(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('posts_dublicate', True, scope)).count()

	def posts_new_link_detected(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('posts_new_link', True, scope)).count()

	def posts_spam_detected(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('posts_spam', True, scope)).count()

	def posts_persisted(self, scope = SCOPE_ALL):
		return self.collection.find(self.get_query('posts_persisted', True, scope)).count()

	def status_full(self):
		status = {}

		status['queries'] = {
			'sent' : { 
				'hour' : self.queries_sent(SCOPE_HOUR),
				'day' : self.queries_sent(SCOPE_DAY),
				'all' : self.queries_sent()
			},
			'completed' : {
				'hour' : self.queries_completed(SCOPE_HOUR),
				'day' : self.queries_completed(SCOPE_DAY),
				'all' : self.queries_completed()
			},
			'error' : {
				'hour' : self.queries_errors(SCOPE_HOUR),
				'day' : self.queries_errors(SCOPE_DAY),
				'all' : self.queries_errors()
			}
		}

		status['http'] = {
			'search' : {
				'yandex' : {
					'sent' : {
						'hour' : self.yandex_search_requests(SCOPE_HOUR),
						'day' : self.yandex_search_requests(SCOPE_DAY)
					},
					'error' : {
						'hour' : self.yandex_search_errors(SCOPE_HOUR),
						'day' : self.yandex_search_errors(SCOPE_DAY)
					}
				}
			},
			'content' : {
				'yandex' : {
					'sent' : {
						'hour' : self.yandex_content_requests(SCOPE_HOUR),
						'day' : self.yandex_content_requests(SCOPE_DAY)
					},
					'error' : {
						'hour' : self.yandex_content_errors(SCOPE_HOUR),
						'day' : self.yandex_content_errors(SCOPE_DAY)
					}
				},
				'lj' : {
					'sent' : {
						'hour' : self.lj_content_requests(SCOPE_HOUR),
						'day' : self.lj_content_requests(SCOPE_DAY)
					},
					'error' : {
						'hour' : self.lj_content_errors(SCOPE_HOUR),
						'day' : self.lj_content_errors(SCOPE_DAY)
					}
				},
				'vk' : {
					'sent' : {
						'hour' : self.vk_content_requests(SCOPE_HOUR),
						'day' : self.vk_content_requests(SCOPE_DAY)
					},
					'error' : {
						'hour' : self.vk_content_errors(SCOPE_HOUR),
						'day' : self.vk_content_errors(SCOPE_DAY)
					}
				}
			}
		}

		status['post'] = {
			'collected' : {
				'hour' : self.posts_collected(SCOPE_HOUR),
				'day' : self.posts_collected(SCOPE_DAY),
				'all' : self.posts_collected()
			},
			'dublicate' : {
				'hour' : self.posts_dublicate_detected(SCOPE_HOUR),
				'day' : self.posts_dublicate_detected(SCOPE_DAY),
				'all' : self.posts_dublicate_detected()
			},
			'update' : {
				'hour' : self.posts_update_detected(SCOPE_HOUR),
				'day' : self.posts_update_detected(SCOPE_DAY),
				'all' : self.posts_update_detected()
			},
			'new_link' : {
				'hour' : self.posts_new_link_detected(SCOPE_HOUR),
				'day' : self.posts_new_link_detected(SCOPE_DAY),
				'all' : self.posts_new_link_detected()
			},
			'spam' : {
				'hour' : self.posts_spam_detected(SCOPE_HOUR),
				'day' : self.posts_spam_detected(SCOPE_DAY),
				'all' : self.posts_spam_detected()
			},
			'persisted' : {
				'hour' : self.posts_persisted(SCOPE_HOUR),
				'day' : self.posts_persisted(SCOPE_DAY),
				'all' : self.posts_persisted()
			},
			'error' : {
				'hour' : 0,
				'day' : 0,
				'all' : 0
			}
		}

		return status
