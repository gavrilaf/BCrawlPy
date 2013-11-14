from bcrawl.base import MQ, Consts
from bcrawl.handlers import BlogHost, Monitor


class Producer(MQ.BaseConsumer):
	def __init__(self):
		super(Producer, self).__init__(Consts.Queues.POSTS_4_FILTER, Consts.Runners.FILTER)

		self.host_detector = BlogHost.Detector()

		self.ya_queue = None
		self.lj_queue = None
		self.vk_queue = None

	def process(self, p):
		self.logger.info('Post for filter: ' + str(p))
		
		is_dublicate = self.is_post_dublicate(p)
		if (is_dublicate):
			self.logger.info('Dublicate found: %s' % p.link)
			self.monitor.dublicate_found(p.link)
			return

		self.remember_post(p)

		p.host = self.detect_blog_host(p)
		self.route_post(p)

	def is_post_dublicate(self, post):
		return False

	def remember_post(self, post):
		pass

	def detect_blog_host(self, post):
		return self.host_detector.get_blog_host(post.link)

	def route_post(self, post):
		if post.host == 'livejournal.com':
			self.logger.info('%s routed to LJ' % post.link)
			self.lj_queue.put(post)
		elif post.host == 'vk.com':
			self.logger.info('%s routed to VK' % post.link)
			self.vk_queue.put(post)
		else:
			self.logger.info('%s routed to Yandex' % post.link)
			self.ya_queue.put(post)

	def on_start(self, connection):
		self.logger.info(self.name + ' is started')

		self.ya_queue = MQ.BaseQueue(connection, Consts.Queues.POSTS_4_CONTENT_COLLECT_YA, self.name)
		self.lj_queue = MQ.BaseQueue(connection, Consts.Queues.POSTS_4_CONTENT_COLLECT_LJ, self.name)
		self.vk_queue = MQ.BaseQueue(connection, Consts.Queues.POSTS_4_CONTENT_COLLECT_VK, self.name)

		self.monitor_queue = MQ.BaseQueue(connection, Consts.Queues.MONITOR, self.name)

		self.monitor = Monitor.Sender(self.monitor_queue)
		
	def on_finish(self):
		self.logger.info(self.name + ' is finished')

		self.ya_queue.close()
		self.lj_queue.close()
		self.vk_queue.close()

		self.monitor_queue.close()