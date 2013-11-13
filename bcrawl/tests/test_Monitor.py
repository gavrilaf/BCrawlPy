import unittest
import datetime
from bcrawl.db import Monitor
from bcrawl.base.MQData import MonitorMsg


class MonitorTests(unittest.TestCase):

	def setUp(self):
		self.db = Monitor.Repository(db_name = 'bcrawl_test', collection_name = 'monitor_test')

	def tearDown(self):
		self.db.clear_monitor_table()
		self.db.close()
		self.db = None

	def testSendQuery(self):
		pass