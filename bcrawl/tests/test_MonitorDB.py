import unittest
import datetime
from bcrawl.monitor import MonDB
from bcrawl.base import Consts
from bcrawl.base.MQData import MonitorMsg


class MonitorDBTests(unittest.TestCase):

	def setUp(self):
		self.db = MonDB.Repository(db_name = Consts.MongoDBs.TEST, collection_name = Consts.MgColls.MONITOR)

	def tearDown(self):
		self.db.clear_table()
		self.db.close()
		self.db = None

	def test_http_requests(self):
		self.assertEqual(self.db.yandex_search_requests(True), 0)
		self.assertEqual(self.db.yandex_content_requests(True), 0)
		self.assertEqual(self.db.lj_content_requests(True), 0)
		self.assertEqual(self.db.vk_content_requests(True), 0)

		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_SEARCH, Consts.Providers.YANDEX, MonitorMsg.OK, 1, None))
		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_CONTENT, Consts.Providers.YANDEX, MonitorMsg.OK, None, 'http://test'))
		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_CONTENT, Consts.Providers.VK, MonitorMsg.OK, None, 'http://test'))
		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_CONTENT, Consts.Providers.LJ, MonitorMsg.OK, None, 'http://test'))

		self.assertEqual(self.db.yandex_search_requests(True), 1)
		self.assertEqual(self.db.yandex_content_requests(True), 1)
		self.assertEqual(self.db.lj_content_requests(True), 1)
		self.assertEqual(self.db.vk_content_requests(True), 1)

	def test_http_requests_err(self):
		self.assertEqual(self.db.yandex_search_requests(False), 0)
		self.assertEqual(self.db.yandex_content_requests(False), 0)
		self.assertEqual(self.db.lj_content_requests(False), 0)
		self.assertEqual(self.db.vk_content_requests(False), 0)

		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_SEARCH, Consts.Providers.YANDEX, MonitorMsg.ERROR, 1, 'error'))
		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_CONTENT, Consts.Providers.YANDEX, MonitorMsg.ERROR, None, 'error'))
		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_CONTENT, Consts.Providers.VK, MonitorMsg.ERROR, None, 'error'))
		self.db.store_msg(MonitorMsg(MonitorMsg.HTTP_CONTENT, Consts.Providers.LJ, MonitorMsg.ERROR, None, 'error'))

		self.assertEqual(self.db.yandex_search_requests(False), 1)
		self.assertEqual(self.db.yandex_content_requests(False), 1)
		self.assertEqual(self.db.lj_content_requests(False), 1)
		self.assertEqual(self.db.vk_content_requests(False), 1)

	def test_queries(self):
		self.assertEqual(self.db.queries_sent(), 0)
		self.assertEqual(self.db.queries_completed(), 0)

		self.db.store_msg(MonitorMsg(MonitorMsg.QUERY_SENT, -1, MonitorMsg.OK, 1, None))
		self.db.store_msg(MonitorMsg(MonitorMsg.QUERY_COMPLETED, -1, MonitorMsg.OK, 1, None))

		self.assertEqual(self.db.queries_sent(), 1)
		self.assertEqual(self.db.queries_completed(), 1)

	def test_posts(self):
		self.assertEqual(self.db.posts_collected(), 0)
		self.assertEqual(self.db.posts_dublicate_detected(), 0)
		self.assertEqual(self.db.posts_update_detected(), 0)
		self.assertEqual(self.db.posts_new_link_detected(), 0)
		self.assertEqual(self.db.posts_persisted(), 0)

		self.db.store_msg(MonitorMsg(MonitorMsg.POST_COLLECTED, -1, MonitorMsg.OK, 1, None))
		self.db.store_msg(MonitorMsg(MonitorMsg.POST_DUBLICATE_DETECTED, -1, MonitorMsg.OK, 1, None))
		self.db.store_msg(MonitorMsg(MonitorMsg.POST_UPDATE_DETECTED, -1, MonitorMsg.OK, 1, None))
		self.db.store_msg(MonitorMsg(MonitorMsg.POST_NEW_LINK_DETECTED, -1, MonitorMsg.OK, 1, None))
		self.db.store_msg(MonitorMsg(MonitorMsg.POST_SPAM_DETECTED, -1, MonitorMsg.OK, 1, None))
		self.db.store_msg(MonitorMsg(MonitorMsg.POST_PERSISTED, -1, MonitorMsg.OK, 1, None))
		

		self.assertEqual(self.db.posts_collected(), 1)
		self.assertEqual(self.db.posts_dublicate_detected(), 1)
		self.assertEqual(self.db.posts_update_detected(), 1)
		self.assertEqual(self.db.posts_new_link_detected(), 1)
		self.assertEqual(self.db.posts_persisted(), 1)

	def test_hour_requests(self):
		self.assertEqual(self.db.yandex_search_requests(True), 0)

		msg = MonitorMsg(MonitorMsg.HTTP_SEARCH, Consts.Providers.YANDEX, MonitorMsg.OK, 1, None)
		self.db.store_msg(msg)

		one_hour = datetime.datetime.utcnow() - datetime.timedelta(minutes = 59, seconds = 59)
		two_hours = datetime.datetime.utcnow() - datetime.timedelta(hours = 2)

		msg.timestamp = one_hour
		self.db.store_msg(msg)

		msg.timestamp = two_hours
		self.db.store_msg(msg)

		self.assertEqual(self.db.yandex_search_requests(True, MonDB.SCOPE_HOUR), 2)

	def test_day_requests(self):
		self.assertEqual(self.db.yandex_search_requests(True), 0)

		msg = MonitorMsg(MonitorMsg.HTTP_SEARCH, Consts.Providers.YANDEX, MonitorMsg.OK, 1, None)
		self.db.store_msg(msg)

		one_day = datetime.datetime.utcnow() - datetime.timedelta(hours = 23, minutes = 59, seconds = 59)
		two_days = datetime.datetime.utcnow() - datetime.timedelta(days = 2)

		msg.timestamp = one_day
		self.db.store_msg(msg)

		msg.timestamp = two_days
		self.db.store_msg(msg)

		self.assertEqual(self.db.yandex_search_requests(True ,MonDB.SCOPE_DAY), 2)


	def test_status_full(self):
		status = self.db.status_full()

		self.assertEqual(status['queries']['sent']['day'], 0)
		self.assertEqual(status['queries']['completed']['all'], 0)

		self.assertEqual(status['http']['search']['yandex']['sent']['hour'], 0)
		self.assertEqual(status['http']['search']['yandex']['error']['day'], 0)
		self.assertEqual(status['http']['content']['yandex']['error']['day'], 0)
		self.assertEqual(status['http']['content']['lj']['sent']['day'], 0)
		self.assertEqual(status['http']['content']['vk']['error']['hour'], 0)

