#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import Consts, MQData
from bcrawl.providers import Yandex
import BaseCollector

class Runner(BaseCollector.BaseRunner):
	def __init__(self):
		super(Runner, self).__init__(Consts.Queues.POSTS_4_CONTENT_COLLECT_YA, 
			Consts.Queues.POSTS_4_PERSIST, 
			Consts.Runners.YA_CONTENT_COLLECTOR,
			MQData.PROVIDER_YANDEX)
		
	def create_reader(self, monitor):
		self.reader = Yandex.ContentReader(self.name, self.monitor)

	def read_content(self, link):
		return self.reader.read_content(link)
