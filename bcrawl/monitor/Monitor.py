from bcrawl.base import MQ
from bcrawl.base import Consts
from bcrawl.monitor import MonDB

class Runner(MQ.BaseConsumer):
	def __init__(self):
		super(Runner, self).__init__(Consts.Queues.MONITOR, Consts.Runners.MONITOR)

	def process(self, p):
		self.repository.store_msg(p)
		self.logger.info(unicode(p))

	def on_start(self, conn):
		self.logger.info(self.name + ' is started')
		self.repository = MonDB.Repository()

	def on_finish(self):
		self.repository.close()
		self.logger.info(self.name + ' is finished')