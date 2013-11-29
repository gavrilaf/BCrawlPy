import unittest
import datetime
from dateutil.tz import *
from bcrawl.base import MQData, Consts
from bcrawl.router import PostInfoDB
from bcrawl.router import Dublicates


class DublicateCheckerTests(unittest.TestCase):

	def setUp(self):
		self.db = PostInfoDB.Repository(db_name = 'bcrawl_test', collection_name = 'post_info_test')
		self.dub_handler = Dublicates.Handler(self.db)

	def tearDown(self):
		self.db.clear_table()
		self.db.close()
		self.db = None

	def testDublicates(self):
		post = MQData.Post.from_values(1, Consts.Providers.YANDEX, ['http://url', 'test', '21.10.2013 00:00Z', 'author'])
		updated = MQData.Post.from_values(1, Consts.Providers.YANDEX, ['http://url', 'test', '22.10.2013 00:00Z', 'author'])
		new_link = MQData.Post.from_values(2, Consts.Providers.YANDEX, ['http://url', 'test', '22.10.2013 00:00Z', 'author'])
		updated_new_link = MQData.Post.from_values(3, Consts.Providers.YANDEX, ['http://url', 'tst', '25.10.2013 00:00Z', 'author'])

		p = self.dub_handler.process(post)
		self.assertEqual(p.status, MQData.Post.NEW)

		p = self.dub_handler.process(post)
		self.assertEqual(p.status, MQData.Post.DUBLICATE)

		p = self.dub_handler.process(updated)
		self.assertEqual(p.status, MQData.Post.UPDATED)

		p = self.dub_handler.process(new_link)
		self.assertEqual(p.status, MQData.Post.NEW_LINK)

		p = self.dub_handler.process(updated_new_link)
		self.assertEqual(p.status, MQData.Post.UPDATED)

		pinfo = self.db.find_pinfo(post.link)

		self.assertIsNotNone(pinfo)

		self.assertEqual(pinfo.publish_date, datetime.datetime(2013, 10, 25, tzinfo=tzutc()))
		self.assertEqual(len(pinfo.queries), 3)
		self.assertTrue(1 in pinfo.queries)
		self.assertTrue(2 in pinfo.queries)
		self.assertTrue(3 in pinfo.queries)