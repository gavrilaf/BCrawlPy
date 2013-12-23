#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import MQ, Consts, MQData
from bcrawl.monitor import MonSender
from bcrawl.router import BlogHost, Dublicates, PostInfoDB, Filters

class Runner(MQ.BaseConsumer):
	def __init__(self):
		super(Runner, self).__init__(Consts.Queues.POSTS_4_ROUTE, Consts.Runners.ROUTER)

		self._db = None

		self._host_detector = None
		self._dub_handler = None
		self._spam_handler = None

		self._yandex_queue = None
		self._common_queues = None

	def process(self, p):
		self.logger.info('Router: %s' % p.link)
		
		# check dublicates & updates
		p = self._dub_handler.process(p)
		self.notify_monitor(p)
		
		if p.status == MQData.Post.DUBLICATE: # Full dublicate found - do nothing
			self.logger.info('Dublicate detected')
			return 

		# detect blog host
		p.host = self._host_detector.get_blog_host(p.link)

		# check spam
		if self._spam_handler.is_spam(p):
			self.logger.info('Spam detected')
			self._monitor.post_spam_detected(p.link)
			return

		# route to queue
		self.route_post(p)

	def route_post(self, post):
		if post.host in Consts.Providers.CONTENT_PROVIDERS:
			self.logger.info('%s (%s): routed to common collector' % (post.link, post.host))
			self._common_queue.put(post)
		else:
			self.logger.info('%s: routed to Yandex' % post.link)
			self._ya_queue.put(post)

	def notify_monitor(self, p):
		if p.status == MQData.Post.DUBLICATE:
			self._monitor.post_dublicate_detected(p.link)
		elif p.status == MQData.Post.UPDATED:
			self._monitor.post_update_detected(p.link)
		elif p.status == MQData.Post.NEW_LINK:
			self._monitor.post_new_link_detected(p.link)

	def on_start(self, connection):
		super(Runner, self).on_start(connection)

		self._db = PostInfoDB.Repository(Consts.MongoDBs.MAIN, Consts.MgColls.POST_INFO)

		self._host_detector = BlogHost.Detector()
		self._dub_handler = Dublicates.Handler(self._db)
		self._spam_handler = Filters.SpamFiltersChain()

		self._ya_queue = MQ.BaseQueue(connection, Consts.Queues.POSTS_4_CONTENT_COLLECT_YA, self.name)
		self._common_queue = MQ.BaseQueue(connection, Consts.Queues.POSTS_4_CONTENT_COLLECT_COMMON, self.name)
		
		self._monitor_queue = MQ.BaseQueue(connection, Consts.Queues.MONITOR, self.name)
		self._monitor = MonSender.Sender(self._monitor_queue)
		
	def on_finish(self):
		self.logger.info(self.name + ' is finished')

		self._ya_queue.close()
		self._common_queue.close()

		self._monitor_queue.close()

		super(Runner, self).on_finish()