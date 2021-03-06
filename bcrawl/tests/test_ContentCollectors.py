#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from bcrawl.base import Consts
from bcrawl.providers import Yandex, LJ, VK, Blogspot, Errors
from bcrawl.monitor import MonSender
from MockQueue import MockQueue



class ContentCollectorTests(unittest.TestCase):

	def setUp(self):
		self.queue = MockQueue()
		self.monitor = MonSender.Sender(self.queue)

	def test_collect_yandex(self):
		pass
		# Сообщения постоянно устаревают, нужно написать тест, который берёт данные из актуального  поиска

		#reader = Yandex.ContentReader(Consts.Runners.TEST, self.monitor)
	
		#self.assertIsNotNone(reader.read_content('http://probyjdenie.livejournal.com/1170195.html'))
		#self.assertIsNone(reader.read_content('http://mayo__not_exists.livejournal.com/463351.html'))

		#self.assertEqual(len(self.queue.items), 2)

	def test_collect_lj(self):
		reader = LJ.ContentReader(Consts.Runners.TEST, self.monitor)

		self.assertIsNotNone(reader.read_content('http://probyjdenie.livejournal.com/1170195.html'))
		self.assertIsNone(reader.read_content('http://mayo__not_exists.livejournal.com/463351.html'))

		self.assertEqual(len(self.queue.items), 2)

	def test_retrieve_vk_id(self):
		reader = VK.ContentReader(Consts.Runners.TEST, self.monitor)

		self.assertEqual(reader.get_vk_id('http://vk.com/wall-34435361_16765'), '-34435361_16765')
		self.assertEqual(reader.get_vk_id('http://vk.com/wall-43647719_543662'), '-43647719_543662')
		
		with self.assertRaises(Errors.InvalidUrl):
			i = reader.get_vk_id('http://vk.com/invalid-post')

	def test_collect_vk(self):
		reader = VK.ContentReader(Consts.Runners.TEST, self.monitor)

		self.assertIsNotNone(reader.read_content('http://vk.com/wall-34435361_16765'))
		self.assertIsNone(reader.read_content('http://vk.com/wall-not_exists_16765'))

		with self.assertRaises(Errors.InvalidUrl):
			i = reader.read_content('http://vk.com/invalid-post')

		self.assertEqual(len(self.queue.items), 2)

	def test_collect_blogspot(self):
		reader = Blogspot.ContentReader(Consts.Runners.TEST, self.monitor)
		content = reader.read_content('http://parasolkin.blogspot.ru/2013/11/2.html')
		self.assertIsNotNone(content)


