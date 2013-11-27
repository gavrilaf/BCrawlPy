#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import Consts, MQData
from bcrawl.providers import VK
import BaseCollector

class Runner(BaseCollector.BaseRunner):
	def __init__(self):
		super(Runner, self).__init__(Consts.Queues.POSTS_4_CONTENT_COLLECT_VK, 
			Consts.Queues.POSTS_4_PERSIST, 
			Consts.Runners.VK_CONTENT_COLLECTOR,
			MQData.PROVIDER_VK)
		
	def create_reader(self, monitor):
		self.reader = VK.ContentReader(self.name, self.monitor)

	def read_content(self, link):
		return self.reader.read_content(link)
