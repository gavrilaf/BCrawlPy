


class SpamFiltersChain(object):
	def __init__(self):
		self._filters = [ DomainSpamFilter() ]

	def is_spam(self, post):
		for filter in self._filters:
			if filter.is_spam(post):
				return True

		return False


class DomainSpamFilter(object):
	def __init__(self):
		self.spam_hosts = ['3dn.ru', 'my1.ru']

	def is_spam(self, post):
		if post.host in self.spam_hosts:
			return True

		return False