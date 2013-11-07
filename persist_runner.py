
import logging.config
from bcrawl.base import MQ, Consts

class PostsPersistConsumer(MQ.BaseConsumer):
	def __init__(self):
		super(PostsPersistConsumer, self).__init__(Consts.Queues.POSTS_4_PERSIST, Consts.Runners.PERSISTER)
		self.fp = None

	def process(self, p):
		self.logger.info('Storing:' + str(p))
		self.fp.write(str(p) + '\n')
		self.fp.write('Collected: %s \n' % str(p.collected))
		if p.content is None:
			self.logger.info('Content is empty')
		else:
			self.fp.write(p.content.encode('utf-8') + '\n')
		self.fp.write('---------------------------------------------------------------------\n')

	def on_start(self, conn):
		self.logger.info(self.name + ' is started')
		self.fp = open('posts.txt', 'w')

	def on_finish(self):
		self.fp.close()
		self.logger.info(self.name + ' is finished')


if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = PostsPersistConsumer()
	p.run()
