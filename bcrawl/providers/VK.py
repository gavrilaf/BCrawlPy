import requests
import logging
import json
import Errors
from bcrawl.base import Consts



class ContentReader(object):
	def __init__(self, runner_name):
		self.logger = logging.getLogger(runner_name)

	def read_content(self, url):
		post_id = self.get_vk_id(url)

		retr_url = 'https://api.vk.com/method/wall.getById?posts=' + post_id

		r = requests.get(retr_url)
		self.logger.info(('(%s, %d)' % (r.url, r.status_code)).encode('utf-8'))
		if r.status_code != 200:
			raise Errors.HttpError(r)

		try:
			return self.parse_response(r)
		except Errors.InvalidJson as e:
			self.logger.warning(e.msg)

	def parse_response(self, r):
		data = json.loads(r.text.encode('utf-8'))
		resp = data['response']
		if resp is None:
			raise Errors.InvalidJson("Can't find 'response' field")

		if len(resp)==0:
			raise Errors.InvalidJson("Field 'response' is empty")	

		return resp[0]['text']		

	def get_vk_id(self, url):
		lst = url.rsplit('wall',1)
		if len(lst) != 2:
			raise Errors.InvalidUrl(url)
		return lst[1]