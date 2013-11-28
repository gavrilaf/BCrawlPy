#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
		
		self.engine = create_engine(self.db_path)
		DB.Base.metadata.create_all(self.engine)
		Session = sessionmaker(bind=self.engine)
		self.session = Session()

		self.db = Posts.Repository(self.session)

	def on_finish(self):
		self.session.close()
		super(PostPersister, self).on_finish()

