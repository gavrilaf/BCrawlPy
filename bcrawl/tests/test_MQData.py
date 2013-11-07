import unittest
import datetime
from bcrawl.base import MQData


class MQDataTests(unittest.TestCase):


	def test_mq_data(self):
		values = ['http://url', 'title', '21.10.2013 19:34', 'author']

		p = MQData.Post.from_values(1, MQData.Post.YANDEX, values)
	
		self.assertEqual('{1, http://url, title, 2013-10-21 19:34:00, author, None}', str(p))  

		self.assertEqual(p.query_id, 1)
		self.assertEqual(p.type, MQData.Post.YANDEX)
		self.assertEqual(p.title, 'title')
		self.assertEqual(p.link, 'http://url')
		self.assertEqual(p.publish_date, datetime.datetime(2013, 10, 21, 19, 34))
		self.assertEqual(p.author, 'author')
