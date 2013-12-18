#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time

from bcrawl.base import MQ, MQData, Consts
from bcrawl.monitor import MonSender
from bcrawl.db import DB, Queries, SearchDB


class Runner(MQ.BaseConsumer):
	_MAX_LOAD = 3

	def __init__(self, db_path):
		super(Runner, self).__init__(Consts.Queues.QUERY_STATUSES, Consts.Runners.SEARCH_CONTROLLER)

		self._db_path = db_path
		
		self._sent_queries_count = 0
		self._got_statuses_count = 0

	def process(self, p):
		'''
			Process query status messages
		'''
		self.logger.info(u"Got query status: %s", unicode(p))

		if p.status == MQData.DayQueryStatus.OK:
			self._monitor.query_completed(p.id)
			self._db.update_day_query_status(p.id, SearchDB.DayQuery.STATUS_COMPLETED)
		elif p.status == MQData.DayQueryStatus.ERROR:
			self._monitor.query_error(p.id)
			self._db.update_day_query_status(p.id, SearchDB.DayQuery.STATUS_NEW)

		self._got_statuses_count += 1

	def on_start(self, connection):
		super(Runner, self).on_start(connection)

		self._db_context = DB.Context(self._db_path)
		self._db = Queries.Repository(self._db_context.session)

		self._queries_queue = MQ.BaseQueue(connection, Consts.Queues.QUERIES, self.name)
		self._monitor_queue = MQ.BaseQueue(connection, Consts.Queues.MONITOR, self.name)
		
		self._monitor = MonSender.Sender(self._monitor_queue)

		self.update_queries()

	def on_finish(self):
		self._queries_queue.close()
		self._monitor_queue.close()

		self._db_context.close()

		super(Runner, self).on_finish()

	def on_idle(self):
		if self._sent_queries_count - self._got_statuses_count < Runner._MAX_LOAD:
			queries = self.get_new_queries()
			if queries:
				self.send_queries(queries)
		
		super(Runner, self).on_idle()
				
	def send_queries(self, queries):
		for dbq in queries:
			query = MQData.DayQuery(dbq.id, dbq.query.id, dbq.query.text, dbq.day)

			self._queries_queue.put(query)
			self._db.update_day_query_status(dbq.id, SearchDB.DayQuery.STATUS_IN_PROGRESS)
			
			self.logger.info(u"Query sent: %s", unicode(query))
			self._monitor.query_sent(query.id)

			self._sent_queries_count += 1

			if self._sent_queries_count - self._got_statuses_count >= Runner._MAX_LOAD:
				break

	def get_new_queries(self):
		return self._db.get_all_day_queries_with_status(SearchDB.DayQuery.STATUS_NEW)

	def update_queries(self):
		queries = self._db.get_queries_by_provider(Consts.Providers.YANDEX)
		for query in queries:
			days = query.get_days_to_now()
			for day in days:
				self._db.add_day_query(query.id, day)



