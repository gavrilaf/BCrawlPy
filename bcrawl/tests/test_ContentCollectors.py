import unittest
from MockQueue import MockQueue
from bcrawl.base import Consts
from bcrawl.providers import Yandex, LJ, VK, Errors
from bcrawl.handlers import Monitor


class ContentCollectorTests(unittest.TestCase):

	def setUp(self):
		self.monitor = Monitor.Sender(MockQueue())

	def test_collect_yandex(self):
		reader = Yandex.ContentReader(Consts.Runners.TEST, self.monitor)
	
		self.assertIsNotNone(reader.read_content('http://vpratus.livejournal.com/30996.html'))
		self.assertIsNone(reader.read_content('http://mayo__not_exists.livejournal.com/463351.html'))

	def test_collect_lj(self):
		reader = LJ.ContentReader(Consts.Runners.TEST)

		self.assertIsNotNone(reader.read_content('http://mayo.livejournal.com/463351.html'))
		self.assertIsNone(reader.read_content('http://mayo__not_exists.livejournal.com/463351.html'))

	def test_retrieve_vk_id(self):
		reader = VK.ContentReader(Consts.Runners.TEST)

		self.assertEqual(reader.get_vk_id('http://vk.com/wall-34435361_16765'), '-34435361_16765')
		self.assertEqual(reader.get_vk_id('http://vk.com/wall-43647719_543662'), '-43647719_543662')
		
		with self.assertRaises(Errors.InvalidUrl):
			i = reader.get_vk_id('http://vk.com/invalid-post')

	def test_collect_vk(self):
		reader = VK.ContentReader(Consts.Runners.TEST)

		self.assertIsNotNone(reader.read_content('http://vk.com/wall-34435361_16765'))
		self.assertIsNone(reader.read_content('http://vk.com/wall-not_exists_16765'))

		with self.assertRaises(Errors.InvalidUrl):
			i = reader.get_vk_id('http://vk.com/invalid-post')

