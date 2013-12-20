from bcrawl.base import MQData, Consts
from bcrawl.base.MQData import MonitorMsg

class Sender(object):
	"""
		Helper class for sending monitoring messages.
	"""
	def __init__(self, queue):
		self.queue = queue 

	
	def query_sent(self, query_id):
		self.queue.put(MonitorMsg(MonitorMsg.QUERY_SENT, -1, MonitorMsg.OK, query_id, None)) 

	def query_completed(self, query_id):
		self.queue.put(MonitorMsg(MonitorMsg.QUERY_COMPLETED, -1,  MonitorMsg.OK, query_id, None)) 

	def query_error(self, query_id):
		self.queue.put(MonitorMsg(MonitorMsg.QUERY_COMPLETED, -1, MonitorMsg.ERROR, query_id, None)) 

	def search_http_request(self, provider, query_id):
		self.queue.put(MonitorMsg(MonitorMsg.HTTP_SEARCH, provider, MonitorMsg.OK, query_id, None)) # now only Yandex search is supported

	def search_http_error(self, provider, query_id, code, url):
		self.queue.put(MonitorMsg(MonitorMsg.HTTP_SEARCH, provider, MonitorMsg.ERROR, query_id, "%s, %s" % (code, url))) # now only Yandex search is supported

	def search_exception(self, provider, query_id, e):
		self.queue.put(MonitorMsg(MonitorMsg.HTTP_SEARCH, provider, MonitorMsg.ERROR, query_id, str(e)))

	def content_http_request(self, provider, link):
		self.queue.put(MonitorMsg(MonitorMsg.HTTP_CONTENT, provider, MonitorMsg.OK, None, link))

	def content_http_error(self, provider, code, url):
		self.queue.put(MonitorMsg(MonitorMsg.HTTP_CONTENT, provider, MonitorMsg.ERROR, None, "%s, %s" % (code, url)))

	def content_exception(self, provider, link, e):
		self.queue.put(MonitorMsg(MonitorMsg.HTTP_CONTENT, provider, MonitorMsg.ERROR, None, str(e)))

	def post_collected(self, link):
		self.queue.put(MonitorMsg(MonitorMsg.POST_COLLECTED, -1, MonitorMsg.OK, None, link))

	def post_dublicate_detected(self, link):
		self.queue.put(MonitorMsg(MonitorMsg.POST_DUBLICATE_DETECTED, -1, MonitorMsg.OK, None, link))

	def post_update_detected(self, link):
		self.queue.put(MonitorMsg(MonitorMsg.POST_UPDATE_DETECTED, -1, MonitorMsg.OK, None, link))

	def post_new_link_detected(self, link):
		self.queue.put(MonitorMsg(MonitorMsg.POST_NEW_LINK_DETECTED, -1, MonitorMsg.OK, None, link))

	def post_spam_detected(self, link):
		self.queue.put(MonitorMsg(MonitorMsg.POST_SPAM_DETECTED, -1, MonitorMsg.OK, None, link))

	def post_persisted(self, post_id, link):
		self.queue.put(MonitorMsg(MonitorMsg.POST_PERSISTED, -1, MonitorMsg.OK, post_id, link))
