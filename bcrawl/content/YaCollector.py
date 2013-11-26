from bcrawl.base import MQ, Consts
from bcrawl.providers import Yandex


class Runner(MQ.BaseProducer):
	def __init__(self):
		super(Runner, self).__init__(Consts.Queues.POSTS_4_CONTENT_COLLECT_YA, Consts.Queues.POSTS_4_PERSIST, Consts.Runners.YA_CONTENT_COLLECTOR)
		
	def process(self, p, out_queue):
		#self.logger.info('Post for collecting: ' + str(p))
		
		p.content = self.collector.read_content(p.link)

		self.logger.info('Post %s. Content is collected' % p.link)
		out_queue.put(p)


	def on_start(self, connection):
		self.collector = Yandex.ContentReader(self.name)