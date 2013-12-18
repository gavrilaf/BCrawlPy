import unittest
from bcrawl.router import BlogHost


class HostDetectorTests(unittest.TestCase):

	def test_host_detector(self):
		detector = BlogHost.Detector()

		self.assertEqual(detector.get_blog_host('http://mayo.livejournal.com/463351.html'), 'livejournal.com')
		self.assertEqual(detector.get_blog_host('http://vk.com/wall-34435361_16765'), 'vk.com')		
		self.assertEqual(detector.get_blog_host('http://www.liveinternet.ru/users/kakula/post297653001/'), 'liveinternet.ru')
		self.assertEqual(detector.get_blog_host('http://tannvasu.ya.ru/replies.xml?item_no=3099'), 'ya.ru')

		self.assertEqual(detector.get_blog_host('http://feedproxy.google.com/~r/blogspot/bdnRq/~3/vw4lZgqJqC8/blog-post_29.html'), 'blogspot.com')
		self.assertEqual(detector.get_blog_host('http://testkos305.blogspot.com/2013/12/476-1640_4.html'), 'blogspot.com')
		self.assertEqual(detector.get_blog_host('http://tekotoje.3dn.ru/blog/neizvestnyj_s_virus_unichtozhaet_chelovecheskoe_naselenie_i_prevrashhaet/2013-11-25-5'), '3dn.ru')

	
