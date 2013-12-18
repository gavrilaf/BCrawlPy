from bcrawl.base import MQ, MQData, Consts
from bcrawl.providers import Yandex, Errors
from bcrawl.monitor import MonSender


class Runner(MQ.BaseProducer):
	def __init__(self):
		super(Runner, self).__init__(Consts.Queues.QUERIES, Consts.Queues.POSTS_4_ROUTE, Consts.Runners.YANDEX_SEARCHER)
		
	def process(self, p, out_queue):
		try:
			self._broker.read_day_posts(p, out_queue)
			self._statuses_queue.put(MQData.DayQueryStatus(p.id, MQData.DayQueryStatus.OK))
			
		except Errors.HttpError as e:
			self.logger.error('Http error code %s on url %s' % (e.code, e.url))

			self._statuses_queue.put(MQData.DayQueryStatus(p.id, MQData.DayQueryStatus.ERROR))
			self._monitor.search_http_error(Consts.Providers.YANDEX, p.id, e.code, e.url)
		
		except Exception as e:
			self.logger.exception(e)

			self._statuses_queue.put(MQData.DayQueryStatus(p.id, MQData.DayQueryStatus.ERROR))
			self._monitor.search_exception(Consts.Providers.YANDEX, p.id, e)

	def on_start(self, connection):
		super(Runner, self).on_start(connection)
	
		self._statuses_queue = MQ.BaseQueue(connection, Consts.Queues.QUERY_STATUSES, self.name)
		self._monitor_queue =  MQ.BaseQueue(connection, Consts.Queues.MONITOR, self.name)

		self._monitor = MonSender.Sender(self._monitor_queue)
		self._broker = Yandex.SearchBroker(self.name, self._monitor)
				
	def on_finish(self):
		super(Runner, self).on_finish()

		self._statuses_queue.close()
		self._monitor_queue.close()