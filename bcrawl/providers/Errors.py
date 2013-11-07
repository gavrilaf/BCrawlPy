
class HttpError(Exception):
	def __init__(self, responce):
		self.url = responce.url
		self.code = responce.status_code

class XmlTagError(Exception):
	def __init__(self, tag, e):
		self.tag = tag
		self.exception = e

class InvalidUrl(Exception):
	def __init__(self, url):
		self.url = url
		
class InvalidJson(Exception):
	def __init__(self, msg):
		self.msg = msg