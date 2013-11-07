import logging
import logging.config
from bcrawl.base import MQ, Consts
from bcrawl.providers import LJ


class LjContentProducer(MQ.BaseProducer):
	def __init__(self):
		super(LjContentProducer, self).__init__(Consts.Queues.POSTS_4_CONTENT_COLLECT_LJ, Consts.Queues.POSTS_4_PERSIST, Consts.Runners.LJ_CONTENT_COLLECTOR)
		self.collector = LJ.ContentReader(self.name)

	def process(self, p, out_queue):
		self.logger.info('Post for collecting: ' + str(p))
		p.content = self.collector.read_content(p.link)
		self.logger.info('Post %s. Content is collected' % p.link)
		out_queue.put(p)

if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = LjContentProducer()
	p.run()