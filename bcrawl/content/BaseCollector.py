from bcrawl.base import MQ, MQData, Consts
from bcrawl.monitor import MonSender
from bcrawl.providers import Yandex, Errors


class BaseRunner(MQ.BaseProducer):
	def __init__(self, in_queue, out_queue, runner_name, provider):
		super(BaseRunner, self).__init__(in_queue, out_queue, runner_name)				
		self.provider = provider	

	def process(self, p, out_queue):
		try:
			content = self.read_content(p.link)

			if content is not None:
				self.logger.info('Post %s. Content is collected' % p.link)
				out_queue.put(p)
			else:
				self.logger.error('Empty content for post: %s' % p.link)	
				self.monitor.content_exception(self.provider, p.link, Exception('Empty content'))
				# TODO: Add processing for posts with empty content

		except Errors.HttpError as e:
			self.logger.error('Http error code %s on url %s' % (e.code, e.url))
			self.monitor.content_http_error(self.provider, e.code, e.url)
		
		except Exception as e:
			self.logger.exception(e)
			self.monitor.content_exception(self.provider, p.link, e)


	def on_start(self, connection):
		super(BaseRunner, self).on_start(connection)

		self.monitor_queue =  MQ.BaseQueue(connection, Consts.Queues.MONITOR, self.name)
		self.monitor = MonSender.Sender(self.monitor_queue)

		self.create_reader(self.monitor)

	def on_finish(self):
		super(BaseRunner, self).on_finish()
		self.monitor_queue.close()

	def create_reader(self, monitor):
		pass

	def read_content(self, link):
		return None