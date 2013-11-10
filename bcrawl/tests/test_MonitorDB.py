import unittest
from bcrawl.db import Monitor
from bcrawl.base.MQData import MonitorMsg


class MonitorDBTests(unittest.TestCase):

	def setUp(self):
		self.db = Monitor.Repository(db_name = 'bcrawl_test', collection_name = 'monitor_test')

	def tearDown(self):
		self.db.clear_monitor_table()
		self.db.close()
		self.db = None

	def test_http_requests(self):
		self.assertEqual(self.db.yandex_search_requests(), 0)
		self.assertEqual(self.db.yandex_content_requests(), 0)
		self.assertEqual(self.db.lj_content_requests(), 0)
		self.assertEqual(self.db.vk_content_requests(), 0)

		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_SEARCH_YANDEX, MonitorMsg.OK, 1, None))
		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_CONTENT_YANDEX, MonitorMsg.OK, None, 'http://test'))
		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_CONTENT_VK, MonitorMsg.OK, None, 'http://test'))
		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_CONTENT_LJ, MonitorMsg.OK, None, 'http://test'))

		self.assertEqual(self.db.yandex_search_requests(), 1)
		self.assertEqual(self.db.yandex_content_requests(), 1)
		self.assertEqual(self.db.lj_content_requests(), 1)
		self.assertEqual(self.db.vk_content_requests(), 1)

	def test_http_requests_err(self):
		pass

	def test_queries(self):
		pass

	def test_posts(self):
		pass

	def test_hour_requests(self):
		pass

	def test_day_requests(self):
		pass