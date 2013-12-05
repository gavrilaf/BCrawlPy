#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
from pymongo import MongoClient
from bcrawl.base import MQ
from bcrawl.base import DB
from bcrawl.runners import Queries
import QueriesStatus

class Runner(MQ.BaseLoggedObj):
	def __init__(self, sql_db_path, mongo_db_path):
		super(Runner, self).__init__("reporter")
		
		self.sql_db_path = sql_db_path
		self.mongo_db_path = mongo_db_path

	def run(self):
		self.on_start()

		try:
			while True:
				generator = self.get_next_report()
				
				self.logger.info('Report %s. Starting...' % generator.name)
				
				report = generator.calculate()
				self.save_report(generator.name, report)

				self.logger.info('Report %s calculated.'  % generator.name)

				self.on_idle()
		finally:
			self.on_finish()

	def on_start(self):
		self.logger.info(self.name + ' is started')

		# Init SqlAlchemy DB context
		self.sql_db_context = DB.Context(self.sql_db_path) 

		# Init Mongo client
		self.mongo_client = MongoClient(tz_aware=True)
		self.mongo_db = self.mongo_client[self.mongo_db_path]

		# Init reports list
		self.reports = [QueriesStatus.Generator(Queries.Repository(self.sql_db_context.session))]


	def on_finish(self):
		self.sql_db_context.close()
		self.mongo_client.close()

		self.logger.info(self.name + ' is finished')

	def on_idle(self):
		time.sleep(5)

	def get_next_report(self):
		return self.reports[0]

	def save_report(self, name, report):
		collection = self.mongo_db[name]
		
		mongo_obj = {'timestamp' : datetime.datetime.now(), 'content' : report}
		collection.insert(mongo_obj)
