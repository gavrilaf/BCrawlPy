#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import logging
import json
from Errors import *
from bcrawl.base import Consts
from bcrawl.base import MQData

class ContentReader(object):
	'''
		Class for retreiving post content using VKontakte API.

		Public method:
			* reader.read_content(url)
			* reader.get_vk_id(url)
	'''

	def __init__(self, runner_name, monitor):
		self.logger = logging.getLogger(runner_name)
		self.monitor = monitor

	def read_content(self, url):
		post_id = self.get_vk_id(url)
		retr_url = 'https://api.vk.com/method/wall.getById?posts=' + post_id

		r = requests.get(retr_url)

		self.monitor.content_http_request(MQData.PROVIDER_VK, url)  # Notify monitor about http request
		self.logger.info('ContentReader: (%s, %d)' % (r.url, r.status_code))

		if r.status_code != 200:
			raise HttpError(r)

		try:
			return self._parse_response(r)

		except InvalidJson as e:
			self.logger.warning(e.msg)

	def get_vk_id(self, url):
		lst = url.rsplit('wall',1)
		if len(lst) != 2:
			raise InvalidUrl(url)

		return lst[1]

	def _parse_response(self, r):
		data = json.loads(r.text.encode('utf-8'))
		resp = data['response']
		if resp is None:
			raise InvalidJson("Can't find 'response' field")

		if len(resp)==0:
			raise InvalidJson("Field 'response' is empty")	

		return resp[0]['text']		

