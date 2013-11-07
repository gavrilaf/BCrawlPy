from bcrawl.base import MQ, MQData, Consts, Tools
from bcrawl.providers import Yandex, Errors


class Producer(MQ.BaseProducer):
	def __init__(self):
		super(Producer, self).__init__(Consts.Queues.QUERIES, Consts.Queues.POSTS_4_FILTER, Consts.Runners.YANDEX_SEARCHER)
		
	def process(self, p, out_queue):
		try:
			self.broker.read_day_posts(p, out_queue, self.monitor)

			self.statuses_queue.put(MQData.DayQueryStatus(p.id, MQData.DayQueryStatus.OK))
			
		except Errors.HttpError as e:
			self.logger.error('Http error code %s on url %s' % (e.code, e.url))

			self.statuses_queue.put(MQData.DayQueryStatus(p.id, MQData.DayQueryStatus.ERROR))
			self.monitor.search_http_error(MQData.PROVIDER_YANDEX, p.id, e.code, e.url)
		
		except Exception as e:
			self.logger.exception(e)

			self.statuses_queue.put(MQData.DayQueryStatus(p.id, MQData.DayQueryStatus.ERROR))
			self.monitor.search_exception(MQData.PROVIDER_YANDEX, p.id, e)

	def on_start(self, connection):
		self.logger.info(self.name + ' is started')

		self.statuses_queue = MQ.BaseQueue(connection, Consts.Queues.QUERY_STATUSES, self.name)
		self.monitor = Tools.Monitor(connection, self.name)
		self.broker = Yandex.SearchBroker(self.name, self.monitor)
				
	def on_finish(self):
		self.logger.info(self.name + ' is finished')

		self.statuses_queue.close()
		self.monitor.close()