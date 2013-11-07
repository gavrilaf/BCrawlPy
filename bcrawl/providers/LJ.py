import requests
import logging
from bs4 import BeautifulSoup


class ContentReader(object):
	def __init__(self, runner_name):
		self.logger = logging.getLogger(runner_name)

	def read_content(self, url):
		url += '?format=light'

		r = requests.get(url)
		self.logger.info(('(%s, %d)'.format(r.url, r.status_code)).encode('utf-8'))
		if r.status_code != 200:
			raise HttpError(r)

		return self.parse_response(r)

	def parse_response(self, r):
		doc = BeautifulSoup(r.text.encode('utf-8'))
		lst = doc.select('article .b-singlepost-body')
		if (len(lst) == 0):
			return None
		txt = lst[0].get_text()
		self.logger.debug('Content: %s' % txt)
		return txt

		