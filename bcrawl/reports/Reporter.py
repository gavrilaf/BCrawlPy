#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
from pymongo import MongoClient
from bcrawl.base import MQ
from bcrawl.db import DB
from bcrawl.db import Queries

import QueriesStatus
import PostsTotal

_IDLE_SHORT = 1
_IDLE_LONG = 5

class Runner(MQ.BaseLoggedObj):
	
	def __init__(self, sql_db_path, mongo_db_path):
		super(Runner, self).__init__("reporter")
		
		self._sql_db_path = sql_db_path
		self._mongo_db_path = mongo_db_path

	def run(self):
		self.on_start()

		try:
			while True:
				generator = self.get_next_generator()
				if generator is None:
					self.on_idle(_IDLE_LONG)
					self.reset_counter()
				else:
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
		self._sql_db_context = DB.Context(self._sql_db_path) 

		# Init Mongo client
		self._mongo_client = MongoClient(tz_aware=True)
		self._mongo_db = self._mongo_client[self._mongo_db_path]

		# Init reports list
		self._reports = [
			QueriesStatus.Generator(Queries.Repository(self._sql_db_context.session)),
			PostsTotal.Generator(Queries.Repository(self._sql_db_context.session)),
		]

		self._counter = 0


	def on_finish(self):
		self._sql_db_context.close()
		self._mongo_client.close()

		self.logger.info(self.name + ' is finished')

	def on_idle(self, t = _IDLE_SHORT):
		time.sleep(t)

	def reset_counter(self):
		self._counter = 0

	def get_next_generator(self):
		if self._counter >= len(self._reports):
			return None

		report = self._reports[self._counter]
		self._counter += 1
		return report


	def save_report(self, name, report):
		collection = self._mongo_db[name]

		# clear old reports
		collection.remove()

		# insert new report
		mongo_obj = {'timestamp' : datetime.datetime.now(), 'content' : report}
		collection.insert(mongo_obj)
