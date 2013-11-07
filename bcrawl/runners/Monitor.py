from bcrawl.base import MQ, Consts
from bcrawl.db import Monitor


class Consumer(MQ.BaseConsumer):
	def __init__(self):
		super(Consumer, self).__init__(Consts.Queues.MONITOR, Consts.Runners.MONITOR)

	def process(self, p):
		self.repository.store_msg(p)
		self.logger.info(str(p))

	def on_start(self, conn):
		self.logger.info(self.name + ' is started')
		self.repository = Monitor.Repository()

	def on_finish(self):
		self.repository.close()
		self.logger.info(self.name + ' is finished')