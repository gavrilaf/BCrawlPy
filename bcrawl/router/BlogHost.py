import tldextract

class Detector(object):

	def __init__(self):
		# self.synonyms = {'vkontakte.com' : 'vk.com'}
		pass
		
	def get_blog_host(self, url):
		r = tldextract.extract(url)
		host = '.'.join([r.domain, r.suffix])

		if host.find('blogspot.com') != -1:
				host = 'blogspot.com'
		
		if host == 'google.com':
			if url.find('feedproxy.google.com/~r/blogspot/') != -1:
				host = 'blogspot.com'

		
		return host