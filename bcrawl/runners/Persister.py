#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import MQ, Consts
from bcrawl.base import DB
import Posts

class PostPersister(MQ.BaseConsumer):
	def __init__(self, db_path):
		super(PostPersister, self).__init__(Consts.Queues.POSTS_4_PERSIST, Consts.Runners.PERSISTER)
		self.db_path = db_path

	def process(self, p):
		self.logger.info('Storing: ' + str(p.link))
		
		self.db.add_post(p)

	def on_start(self, connection):
		super(PostPersister, self).on_start(connection)
		
		self.db_context = DB.Context(self.db_path)
		self.db = Posts.Repository(self.db_context.session)

	def on_finish(self):
		self.db_context.close()
		super(PostPersister, self).on_finish()

