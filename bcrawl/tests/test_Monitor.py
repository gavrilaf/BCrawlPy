import unittest
import datetime
from bcrawl.base import MQData, Consts
from bcrawl.monitor import MonDB
from bcrawl.monitor import MonSender

class MockDbQueue(object):
	def __init__(self, db):
		self.db = db

	def put(self, p):
		self.db.store_msg(p)

class MonitorTests(unittest.TestCase):

	def setUp(self):
		self.db = MonDB.Repository(db_name = Consts.MongoDBs.TEST, collection_name = Consts.MgColls.MONITOR)
		self.queue = MockDbQueue(self.db)
		self.monitor = MonSender.Sender(self.queue)

	def tearDown(self):
		self.db.clear_table()
		self.db.close()


	def testSendQuery(self):
		status = self.db.status_full()
		self.assertEqual(status['queries']['sent']['day'], 0)
		self.assertEqual(status['queries']['completed']['all'], 0)

		for i in xrange(10):
			self.monitor.query_sent(i)
			self.monitor.query_completed(i)

		status = self.db.status_full()
		self.assertEqual(status['queries']['sent']['day'], 10)
		self.assertEqual(status['queries']['completed']['all'], 10)


	def testHttpMsgs(self):
		status = self.db.status_full()
		self.assertEqual(status['http']['search']['yandex']['sent']['hour'], 0)
		self.assertEqual(status['http']['search']['yandex']['error']['day'], 0)
		self.assertEqual(status['http']['content']['yandex']['error']['day'], 0)
		self.assertEqual(status['http']['content']['lj']['sent']['day'], 0)
		self.assertEqual(status['http']['content']['vk']['error']['hour'], 0)

		for i in xrange(3):
			self.monitor.search_http_request(Consts.Providers.YANDEX, 1)
			self.monitor.search_http_error(Consts.Providers.YANDEX, 1, 404, 'test_url')
			self.monitor.search_exception(Consts.Providers.YANDEX, 1, Exception('test'))
			self.monitor.content_http_error(Consts.Providers.YANDEX, 404, 'test_url')
			self.monitor.content_http_request(Consts.Providers.LJ, 'test_url')
			self.monitor.content_exception(Consts.Providers.VK, 'test_url', Exception('test'))

		status = self.db.status_full()
		self.assertEqual(status['http']['search']['yandex']['sent']['hour'], 3)
		self.assertEqual(status['http']['search']['yandex']['error']['day'], 6)
		self.assertEqual(status['http']['content']['yandex']['error']['day'], 3)
		self.assertEqual(status['http']['content']['lj']['sent']['day'], 3)
		self.assertEqual(status['http']['content']['vk']['error']['hour'], 3)

	def testPostMsgs(self):
		status = self.db.status_full()
		self.assertEqual(status['post']['collected']['all'], 0)
		self.assertEqual(status['post']['dublicate']['hour'], 0)
		self.assertEqual(status['post']['update']['day'], 0)
		self.assertEqual(status['post']['new_link']['all'], 0)
		self.assertEqual(status['post']['persisted']['all'], 0)

		self.monitor.post_collected('test')
		self.monitor.post_dublicate_detected('test')
		self.monitor.post_update_detected('test')
		self.monitor.post_new_link_detected('test')
		self.monitor.post_persisted(1, 'test')

		status = self.db.status_full()
		self.assertEqual(status['post']['collected']['all'], 1)
		self.assertEqual(status['post']['dublicate']['hour'], 1)
		self.assertEqual(status['post']['update']['day'], 1)
		self.assertEqual(status['post']['new_link']['all'], 1)
		self.assertEqual(status['post']['persisted']['all'], 1)