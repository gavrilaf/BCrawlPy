#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import logging
import Errors
from bs4 import BeautifulSoup
from bcrawl.base import Consts
from bcrawl.base import MQData

class ContentReader(object):
	'''
		Class for retreiving post content using LJ API.

		Public method:
			* reader.read_content(url)
	'''

	def __init__(self, runner_name, monitor):
		self.logger = logging.getLogger(runner_name)
		self.monitor = monitor

	def read_content(self, url):
		url += '?format=light'

		r = requests.get(url)
		
		self.monitor.content_http_request(MQData.PROVIDER_LJ, url)  # Notify monitor about http request
		self.logger.info('ContentReader: (%s, %d)' % (r.url, r.status_code))

		if r.status_code != 200:
			raise HttpError(r)

		return self._parse_response(r)

	def _parse_response(self, r):
		doc = BeautifulSoup(r.text.encode('utf-8'))
		lst = doc.select('article .b-singlepost-body')
		if not lst:
			return None
		
		return lst[0].get_text()
		
		