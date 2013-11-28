#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
from bcrawl.base import MQ, MQData, Consts
from bcrawl.monitor import MonSender
import Queries

class Runner(MQ.BaseConsumer):
	def __init__(self, db_path):
		super(Runner, self).__init__(Consts.Queues.QUERY_STATUSES, Consts.Runners.SEARCH_CONTROLLER)

		self.db_path = db_path
		self.counter = 0

	def process(self, p):
		self.logger.info("Got query status: %s", str(p))
		if p.status == MQData.DayQueryStatus.OK:
			self.monitor.query_completed(p.id)

	def on_start(self, conn):
		super(Runner, self).on_start(connection)

		self.db_context = DB.Context(self.db_path)
		self.db = Posts.Repository(self.db_context.session)

		self.queries_queue = MQ.BaseQueue(conn, Consts.Queues.QUERIES, self.name)
		self.monitor_queue = MQ.BaseQueue(conn, Consts.Queues.MONITOR, self.name)
		
		self.monitor = MonSender.Sender(self.monitor_queue)

	def on_finish(self):
		self.queries_queue.close()
		self.monitor_queue.close()

		self.db_context.close()

		super(Runner, self).on_finish()

	def on_idle(self):
		queries = self.get_new_queries()
		if queries:
			self.send_queries(queries)
		
		super(Runner, self).on_idle()
				
	def send_queries(self, queries):
		for query in queries:
			self.queries_queue.put(query)

			self.logger.info("Query sent: %s", str(query))
			self.monitor.query_sent(query.id)

	def get_new_queries(self):
		if self.counter >= 3:
			return []

		#query = MQData.DayQuery(self.counter+1, self.counter+1, 'джихад', datetime.date.today()-datetime.timedelta(self.counter))
		query = MQData.DayQuery(self.counter+1, 1, 'джихад', datetime.date.today())
		self.counter += 1

		return [query]
