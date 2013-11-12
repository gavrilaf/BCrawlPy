import unittest
import datetime
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
		self.assertEqual(self.db.yandex_search_requests(), 0)
		self.assertEqual(self.db.yandex_content_requests(), 0)
		self.assertEqual(self.db.lj_content_requests(), 0)
		self.assertEqual(self.db.vk_content_requests(), 0)

		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_SEARCH_YANDEX, MonitorMsg.ERROR, 1, 'error'))
		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_CONTENT_YANDEX, MonitorMsg.ERROR, None, 'error'))
		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_CONTENT_VK, MonitorMsg.ERROR, None, 'error'))
		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_CONTENT_LJ, MonitorMsg.ERROR, None, 'error'))

		self.assertEqual(self.db.yandex_search_errors(), 1)
		self.assertEqual(self.db.yandex_content_errors(), 1)
		self.assertEqual(self.db.lj_content_errors(), 1)
		self.assertEqual(self.db.vk_content_errors(), 1)

	def test_queries(self):
		self.assertEqual(self.db.queries_sent(), 0)
		self.assertEqual(self.db.queries_completed(), 0)

		self.db.store_msg(MonitorMsg(MonitorMsg.QUERY_SENT, MonitorMsg.OK, 1, None))
		self.db.store_msg(MonitorMsg(MonitorMsg.QUERY_COMPLETED, MonitorMsg.OK, 1, None))

		self.assertEqual(self.db.queries_sent(), 1)
		self.assertEqual(self.db.queries_completed(), 1)

	def test_posts(self):
		self.assertEqual(self.db.posts_collected(), 0)
		self.assertEqual(self.db.posts_dublicate_detected(), 0)
		self.assertEqual(self.db.posts_update_detected(), 0)
		self.assertEqual(self.db.posts_new_link_detected(), 0)
		self.assertEqual(self.db.posts_persisted(), 0)

		self.db.store_msg(MonitorMsg(MonitorMsg.POST_COLLECTED, MonitorMsg.OK, 1, None))
		self.db.store_msg(MonitorMsg(MonitorMsg.POST_DUBLICATE_DETECTED, MonitorMsg.OK, 1, None))
		self.db.store_msg(MonitorMsg(MonitorMsg.POST_UPDATE_DETECTED, MonitorMsg.OK, 1, None))
		self.db.store_msg(MonitorMsg(MonitorMsg.POST_NEW_LINK_DETECTED, MonitorMsg.OK, 1, None))
		self.db.store_msg(MonitorMsg(MonitorMsg.POST_SPAM_DETECTED, MonitorMsg.OK, 1, None))
		self.db.store_msg(MonitorMsg(MonitorMsg.POST_PERSISTED, MonitorMsg.OK, 1, None))
		

		self.assertEqual(self.db.posts_collected(), 1)
		self.assertEqual(self.db.posts_dublicate_detected(), 1)
		self.assertEqual(self.db.posts_update_detected(), 1)
		self.assertEqual(self.db.posts_new_link_detected(), 1)
		self.assertEqual(self.db.posts_persisted(), 1)

	def test_hour_requests(self):
		self.assertEqual(self.db.yandex_search_requests(), 0)

		msg = MonitorMsg(MonitorMsg.HTTP_SEARCH_YANDEX, MonitorMsg.OK, 1, None)
		self.db.store_msg(msg)

		one_hour = datetime.datetime.utcnow() - datetime.timedelta(minutes = 59, seconds = 59)
		two_hours = datetime.datetime.utcnow() - datetime.timedelta(hours = 2)

		msg.timestamp = one_hour
		self.db.store_msg(msg)

		msg.timestamp = two_hours
		self.db.store_msg(msg)

		self.assertEqual(self.db.yandex_search_requests(Monitor.Repository.HOUR), 2)

	def test_day_requests(self):
		self.assertEqual(self.db.yandex_search_requests(), 0)

		msg = MonitorMsg(MonitorMsg.HTTP_SEARCH_YANDEX, MonitorMsg.OK, 1, None)
		self.db.store_msg(msg)

		one_day = datetime.datetime.utcnow() - datetime.timedelta(hours = 23, minutes = 59, seconds = 59)
		two_days = datetime.datetime.utcnow() - datetime.timedelta(days = 2)

		msg.timestamp = one_day
		self.db.store_msg(msg)

		msg.timestamp = two_days
		self.db.store_msg(msg)

		self.assertEqual(self.db.yandex_search_requests(Monitor.Repository.DAY), 2)