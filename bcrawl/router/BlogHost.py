import tldextract

class Detector(object):

	def __init__(self):
		self.synonyms = {'vkontakte.com' : 'vk.com'}
		
	def get_blog_host(self, url):
		r = tldextract.extract(url)
		host = '.'.join([r.domain, r.suffix])
		if host in self.synonyms:
			return self.synonyms[host]
		return host