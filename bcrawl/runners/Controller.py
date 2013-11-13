#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
from bcrawl.base import MQ, MQData, Consts
from bcrawl.handlers import Monitor

class Runner(MQ.BaseConsumer):
	def __init__(self):
		super(Runner, self).__init__(Consts.Queues.QUERY_STATUSES, Consts.Runners.SEARCH_CONTROLLER)

		self.counter = 0

	def process(self, p):
		self.logger.info("Got query status: %s", str(p))
		if p.status == MQData.DayQueryStatus.OK:
			self.monitor.query_completed(p.id)

	def on_start(self, conn):
		self.logger.info(self.name + ' is started')

		self.queries_queue = MQ.BaseQueue(conn, Consts.Queues.QUERIES, self.name)
		self.monitor_queue = MQ.BaseQueue(conn, Consts.Queues.MONITOR, self.name)
		
		self.monitor = Monitor.Sender(self.monitor_queue)

	def on_finish(self):
		self.queries_queue.close()
		self.monitor_queue.close()

		self.logger.info(self.name + ' is finished')

	def on_idle(self):
		queries = self.get_new_queries()
		if queries:
			self.send_queries(queries)
		else:
			time.sleep(1)
				
	def send_queries(self, queries):
		for query in queries:
			self.queries_queue.put(query)

			self.logger.info("Query sent: %s", str(query))
			self.monitor.query_sent(query.id)

	def get_new_queries(self):
		if self.counter >= 3:
			return []

		query = MQData.DayQuery(1, self.counter+1, 'джихад', datetime.date.today()-datetime.timedelta(self.counter))
		self.counter += 1

		return [query]
