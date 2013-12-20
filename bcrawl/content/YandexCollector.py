#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import Consts, MQData
from bcrawl.providers import Yandex
import BaseCollector

class Runner(MQ.BaseProducer):
	def __init__(self):
		super(Runner, self).__init__(Consts.Queues.POSTS_4_CONTENT_COLLECT_YA, 
			Consts.Queues.POSTS_4_PERSIST, 
			Consts.Runners.YA_CONTENT_COLLECTOR)


	def process(self, p, out_queue):
		try:
			content = self._reader.read_content(p.link)

			if content is not None:
				self.logger.info('Post %s. Content is collected' % p.link)
			else:
				self.logger.error('Empty content for post: %s' % p.link)	
				self._monitor.content_exception(self.provider, p.link, Exception('Empty content'))
				self.set_content_error(p)

		except Errors.HttpError as e:
			self.logger.error('Http error code %s on url %s' % (e.code, e.url))
			self._monitor.content_http_error(self.provider, e.code, e.url)
			self.set_content_error(p)
		
		except Exception as e:
			self.logger.exception(e)
			self._monitor.content_exception(self.provider, p.link, e)
			self.set_content_error(p)

		out_queue.put(p)

	def set_content_error(self, post):
		post.content = post.title
		post.content_error = True

	def on_start(self, connection):
		super(BaseRunner, self).on_start(connection)

		self._monitor_queue =  MQ.BaseQueue(connection, Consts.Queues.MONITOR, self.name)
		self._monitor = MonSender.Sender(self.monitor_queue)

		self._reader = Yandex.ContentReader(self.name, self._monitor)

		
	def on_finish(self):
		self._monitor_queue.close()

		super(BaseRunner, self).on_finish()

	
