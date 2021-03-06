#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import datetime
from bcrawl.base import MQData, Consts


class MQDataTests(unittest.TestCase):


	def test_mq_data(self):
		values = ['http://url', 'тест', '21.10.2013 19:34', 'author']
 
		p = MQData.Post.from_values(1, Consts.Providers.YANDEX, values)

		s = str(p)
		self.assertEqual('{1, http://url, тест, 2013-10-21 19:34:00, author, None}', s)  

		self.assertEqual(p.query_id, 1)
		self.assertEqual(p.provider, Consts.Providers.YANDEX)
		self.assertEqual(p.title, 'тест')
		self.assertEqual(p.link, 'http://url')
		self.assertEqual(p.publish_date, datetime.datetime(2013, 10, 21, 19, 34))
		self.assertEqual(p.author, 'author')
