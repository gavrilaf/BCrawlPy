from bcrawl.base import MQ
from bcrawl.base import Consts
from bcrawl.monitor import MonDB

class Runner(MQ.BaseConsumer):
	def __init__(self):
		super(Runner, self).__init__(Consts.Queues.MONITOR, Consts.Runners.MONITOR)

	def process(self, p):
		self._repository.store_msg(p)
		self.logger.info(unicode(p))

	def on_start(self, conn):
		super(Runner, self).on_start(connection)
		self._repository = MonDB.Repository(Consts.MongoDBs.MAIN, Consts.MgColls.MONITOR)

	def on_finish(self):
		self._repository.close()
		super(Runner, self).on_finish()