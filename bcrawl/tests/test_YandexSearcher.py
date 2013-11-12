#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import datetime
import MockQueue
from bcrawl.base import Consts, MQData, Tools
from bcrawl.providers import Yandex

class MockQueue(object):
	def __init__(self):
		self.lst = []

	def put(self, obj):
		self.lst.append(obj)



class YandexSearcherTests(unittest.TestCase):

	def setUp(self):
		self.monitor = Tools.Monitor(MockQueue())

	def test_searcher(self):
		searcher = Yandex.Searcher(Consts.Runners.TEST, self.monitor)

		day = datetime.date(2013, 10, 30)
		day_query = MQData.DayQuery(1, 1234, u'путин', day)

		posts = searcher.start_search(day_query)
		
		self.assertIsNotNone(posts)	
		self.assertTrue(len(posts) > 0)

		self.assertEqual(posts[0].publish_date.date(), day)
		self.assertEqual(posts[0].query_id, 1234)

		posts = searcher.next()

		self.assertIsNotNone(posts)	
		self.assertTrue(len(posts) > 0)

		self.assertEqual(posts[0].publish_date.date(), day)
		self.assertEqual(posts[0].query_id, 1234)

	def test_broker(self):
		broker = Yandex.SearchBroker(Consts.Runners.TEST, self.monitor)

		day = datetime.date(2013, 10, 30)
		day_query = MQData.DayQuery(1, 1234, u'котеги', day)

		out_queue = MockQueue()
		status_queue = MockQueue()

		broker.read_day_posts(day_query, out_queue, status_queue)
		
		self.assertIsNotNone(out_queue.lst)	
		self.assertTrue(len(out_queue.lst) > 0)

		self.assertEqual(out_queue.lst[0].publish_date.date(), day)
		self.assertEqual(out_queue.lst[0].query_id, 1234)

		