#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import MQ, Consts
from bcrawl.base import DB
from bcrawl.monitor import MonSender
from bcrawl.db import Posts

class PostPersister(MQ.BaseConsumer):
	def __init__(self, db_path):
		super(PostPersister, self).__init__(Consts.Queues.POSTS_4_PERSIST, Consts.Runners.PERSISTER)
		self._db_path = db_path

	def process(self, p):
		self.logger.info('Storing: ' + str(p.link))
		
		np = self._db.add_post(p)
		self.monitor.post_persisted(np.id, np.link)

	def on_start(self, connection):
		super(PostPersister, self).on_start(connection)

		self._monitor_queue = MQ.BaseQueue(connection, Consts.Queues.MONITOR, self.name)
		
		self._monitor = MonSender.Sender(self._monitor_queue)
		
		self._db_context = DB.Context(self._db_path)
		self._db = Posts.Repository(self._db_context.session)

	def on_finish(self):
		self._monitor_queue.close()
		self._db_context.close()

		super(PostPersister, self).on_finish()

