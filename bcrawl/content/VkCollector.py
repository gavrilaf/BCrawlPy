#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import MQ, Consts
from bcrawl.providers import VK


class Runner(MQ.BaseProducer):
	def __init__(self):
		super(Runner, self).__init__(Consts.Queues.POSTS_4_CONTENT_COLLECT_VK, Consts.Queues.POSTS_4_PERSIST, Consts.Runners.VK_CONTENT_COLLECTOR)
		
	def process(self, p, out_queue):
		#self.logger.info('Post for collecting: ' + str(p))
		
		p.content = self.collector.read_content(p.link)

		self.logger.info('Post %s. Content is collected' % p.link)
		out_queue.put(p)


	def on_start(self, connection):
		self.collector = VK.ContentReader(self.name)