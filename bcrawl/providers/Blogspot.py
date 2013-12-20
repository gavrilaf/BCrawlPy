#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import logging
from Errors import *
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
		self._logger = logging.getLogger(runner_name)
		self._monitor = monitor

	def read_content(self, url):
		r = requests.get(url)
		
		self._monitor.content_http_request(Consts.Providers.BLOGSPOT, url)  # Notify monitor about http request
		self._logger.info('ContentReader: (%s, %d)' % (r.url, r.status_code))

		if r.status_code != 200:
			raise HttpError(r)

		return self._parse_response(r)

	def _parse_response(self, r):
		doc = BeautifulSoup(r.text.encode('utf-8'))
		lst = doc.select('div .post-body.entry-content')
		if not lst:
			return None
		
		return lst[0].get_text()