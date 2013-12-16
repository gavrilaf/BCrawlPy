#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import MQ, Consts, MQData
from bcrawl.monitor import MonSender
from bcrawl.router import BlogHost, Dublicates, PostInfoDB

class Runner(MQ.BaseConsumer):
	def __init__(self):
		super(Runner, self).__init__(Consts.Queues.POSTS_4_ROUTE, Consts.Runners.ROUTER)

		self.db = None

		self.host_detector = None
		self.dub_handler = None

		self.ya_queue = None
		self.lj_queue = None
		self.vk_queue = None

	def process(self, p):
		self.logger.info('Router: %s' % p.link)
		
		p = self.dub_handler.process(p)
		self.notify_monitor(p)

		#print 'Status: %d' % p.status
		if p.status == MQData.Post.DUBLICATE: # Full dublicate found - do nothing
			return 

		p.host = self.host_detector.get_blog_host(p.link)
		self.route_post(p)

	def route_post(self, post):
		if post.host == 'livejournal.com':
			self.logger.info('%s routed to LJ' % post.link)
			self.lj_queue.put(post)
		elif post.host == 'vk.com':
			self.logger.info('%s routed to VK' % post.link)
			self.vk_queue.put(post)
		else:
			self.logger.info('%s routed to Yandex' % post.link)
			self.ya_queue.put(post)

	def notify_monitor(self, p):
		if p.status == MQData.Post.DUBLICATE:
			self.monitor.post_dublicate_detected(p.link)
		elif p.status == MQData.Post.UPDATED:
			self.monitor.post_update_detected(p.link)
		elif p.status == MQData.Post.NEW_LINK:
			self.monitor.post_new_link_detected(p.link)

	def on_start(self, connection):
		self.logger.info(self.name + ' is started')

		self.db = PostInfoDB.Repository('bcrawl', 'post_info')

		self.host_detector = BlogHost.Detector()
		self.dub_handler = Dublicates.Handler(self.db)

		self.ya_queue = MQ.BaseQueue(connection, Consts.Queues.POSTS_4_CONTENT_COLLECT_YA, self.name)
		self.lj_queue = MQ.BaseQueue(connection, Consts.Queues.POSTS_4_CONTENT_COLLECT_LJ, self.name)
		self.vk_queue = MQ.BaseQueue(connection, Consts.Queues.POSTS_4_CONTENT_COLLECT_VK, self.name)

		self.monitor_queue = MQ.BaseQueue(connection, Consts.Queues.MONITOR, self.name)

		self.monitor = MonSender.Sender(self.monitor_queue)
		
	def on_finish(self):
		self.logger.info(self.name + ' is finished')

		self.ya_queue.close()
		self.lj_queue.close()
		self.vk_queue.close()

		self.monitor_queue.close()