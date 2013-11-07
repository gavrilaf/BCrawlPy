import datetime 
from dateutil import parser
import jsonpickle

PROVIDER_YANDEX = 1
PROVIDER_TWITTER = 2
PROVIDER_LJ = 3
PROVIDER_VK = 4

class Post(object):
 	@staticmethod
	def from_values(query_id, provider, values_):
		return Post(query_id, provider, values_[0], values_[1], parser.parse(values_[2]), values_[3])

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

	def __str__(self):
		return (u'{%d, %s, %s, %s, %s, %s}' % (self.query_id, self.link, self.title,  self.publish_date, self.author, self.host)).encode('utf-8')

class DayQuery(object):
	def __init__(self, id_, query_id, text, day):
		self.id = id_
		self.query_id = query_id
		self.text = text
		self.day = day

	def __str__(self):
		return (u'{%d, %d, %s, %s}' % (self.id, self.query_id, self.text, self.day)).encode('utf-8')

class DayQueryStatus(object):
	OK = 1
	ERROR = 2

	def __init__(self, id_, status):
		self.id = id_
		self.status = status

	def __str__(self):
		return '{%d, %d}' % (self.id, self.status)

class MonitorMsg(object):
	HTTP_SEARCH_YANDEX = 1
	HTTP_CONTENT_YANDEX = 2
	HTTP_CONTENT_LJ = 3
	HTTP_CONTENT_VK = 4
	POST_PERSISTED = 5
	QUERY_COMPLETED = 6
	POST_FILTERED = 7

	OK = 1
	ERROR = 2
	
	def __init__(self, type_, status, id_, text):
		self.type = type_
		self.status = status
		self.id = id_
		self.text = text
		self.timestamp = datetime.datetime.utcnow()

	def __str__(self):
		return '{%d, %d, %s, %s, %s}' % (self.type, self.status, self.timestamp, self.id, self.text)

	def mongo_rep(self):
		obj = {'type' : self.type, 'status' : self.status, 'timestamp' : self.timestamp, 'obj_id' : self.id, 'text' : self.text}
		return obj



