#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.config
import datetime
import time
import kombu
from contextlib import closing
from bcrawl.base import MQ, MQData, Consts



class SearchControllerRunner(object):
	def __init__(self):
		self.logger = logging.getLogger(Consts.Runners.SEARCH_CONTROLLER)

	def run(self):
		self.logger.info('SearchController starting...')

		with kombu.Connection() as conn:
			with closing(MQ.BaseQueue(conn, Consts.Queues.QUERIES, Consts.Runners.SEARCH_CONTROLLER)) as queries_queue:
				with closing(MQ.BaseQueue(conn, Consts.Queues.QUERY_STATUSES, Consts.Runners.SEARCH_CONTROLLER)) as statuses_queue:
					while True: 
						self.send_queries(queries_queue)
						self.process_statuses(statuses_queue)
						time.sleep(10)
			
				

	def send_queries(self, queries_queue):

		for i in range(3):
			query = MQData.DayQuery(1, i, u'джихад', datetime.date.today()-datetime.timedelta(i))
			self.logger.info("Put query: %s" % str(query))
			queries_queue.put(query)

	def process_statuses(self, statuses_queue):
		pass



if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = SearchControllerRunner()
	p.run()
	



