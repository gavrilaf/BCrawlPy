#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
from bcrawl.base import MQ, MQData, Consts, DB
from bcrawl.monitor import MonSender
import Queries
import SearchDB

class Runner(MQ.BaseConsumer):
	_MAX_LOAD = 3

	def __init__(self, db_path):
		super(Runner, self).__init__(Consts.Queues.QUERY_STATUSES, Consts.Runners.SEARCH_CONTROLLER)

		self.db_path = db_path
		
		self.sent_queries_count = 0
		self.got_statuses_count = 0

	def process(self, p):
		'''
			Process query status messages
		'''
		self.logger.info(u"Got query status: %s", unicode(p))

		if p.status == MQData.DayQueryStatus.OK:
			self.monitor.query_completed(p.id)
			self.db.update_day_query_status(p.id, SearchDB.DayQuery.STATUS_COMPLETED)
		elif p.status == MQData.DayQueryStatus.ERROR:
			self.monitor.query_error(p.id)
			self.db.update_day_query_status(p.id, SearchDB.DayQuery.STATUS_NEW)

		self.got_statuses_count += 1


	def on_start(self, connection):
		super(Runner, self).on_start(connection)

		self.db_context = DB.Context(self.db_path)
		self.db = Queries.Repository(self.db_context.session)

		self.queries_queue = MQ.BaseQueue(connection, Consts.Queues.QUERIES, self.name)
		self.monitor_queue = MQ.BaseQueue(connection, Consts.Queues.MONITOR, self.name)
		
		self.monitor = MonSender.Sender(self.monitor_queue)

		self.update_queries()

	def on_finish(self):
		self.queries_queue.close()
		self.monitor_queue.close()

		self.db_context.close()

		super(Runner, self).on_finish()

	def on_idle(self):
		if self.sent_queries_count - self.got_statuses_count < Runner._MAX_LOAD:
			queries = self.get_new_queries()
			if queries:
				self.send_queries(queries)
		
		super(Runner, self).on_idle()
				
	def send_queries(self, queries):
		for dbq in queries:
			query = MQData.DayQuery(dbq.id, dbq.query.id, dbq.query.text, dbq.day)

			self.queries_queue.put(query)
			self.db.update_day_query_status(dbq.id, SearchDB.DayQuery.STATUS_IN_PROGRESS)
			
			self.logger.info(u"Query sent: %s", unicode(query))
			self.monitor.query_sent(query.id)

			self.sent_queries_count += 1

			if self.sent_queries_count - self.got_statuses_count >= Runner._MAX_LOAD:
				break



	def get_new_queries(self):
		return self.db.get_all_day_queries_with_status(SearchDB.DayQuery.STATUS_NEW)

	def update_queries(self):
		queries = self.db.get_queries_by_provider(Consts.Providers.YANDEX)
		for query in queries:
			days = query.get_days_to_now()
			for day in days:
				self.db.add_day_query(query.id, day)



