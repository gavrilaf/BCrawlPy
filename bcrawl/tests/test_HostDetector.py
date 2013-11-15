import unittest
from bcrawl.router import BlogHost


class HostDetectorTests(unittest.TestCase):

	def test_host_detector(self):
		detector = BlogHost.Detector()

		self.assertEqual(detector.get_blog_host('http://mayo.livejournal.com/463351.html'), 'livejournal.com')
		self.assertEqual(detector.get_blog_host('http://vk.com/wall-34435361_16765'), 'vk.com')
		self.assertEqual(detector.get_blog_host('http://vkontakte.com/wall-34435361_16765'), 'vk.com')
		self.assertEqual(detector.get_blog_host('http://www.liveinternet.ru/users/kakula/post297653001/'), 'liveinternet.ru')
		self.assertEqual(detector.get_blog_host('http://tannvasu.ya.ru/replies.xml?item_no=3099'), 'ya.ru')
	
