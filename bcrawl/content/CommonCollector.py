from bcrawl.base import MQ, MQData, Consts
from bcrawl.monitor import MonSender
from bcrawl.providers import Errors

from bcrawl.providers import LJ
from bcrawl.providers import VK
from bcrawl.providers import YaBlog
from bcrawl.providers import Blogspot



class Runner(MQ.BaseProducer):
	def __init__(self):
		super(Runner, self).__init__(Consts.Queues.POSTS_4_CONTENT_COLLECT_COMMON, 
			Consts.Queues.POSTS_4_PERSIST, 
			Consts.Runners.COMMON_CONTENT_COLLECTOR)

	def process(self, p, out_queue):
		provider = Consts.Providers.content_provider_by_host(p.host)

		if provider == -1:
			self.logger.error('Post (%s, %s). Unknown provider' % (p.link, p.host))
			raise Exception('Unknown provider')

		if provider not in self._readers:
			self.logger.info('Post %s. Cant find content reader. Redirect to Yandex.' % p.link)
			self._monitor.content_exception(self.provider, p.link, Exception('Cant find content reader. Redirect to Yandex.'))
			self._yandex_queue.put(p)
		else:
			try: 
				reader = self._readers[provider]
				content = reader.read_content(p.link)
				
				if content is not None:
					self.logger.info('Post %s. Content is collected' % p.link)
					print content
					p.content = content
					out_queue.put(p)
				else:	
					self.logger.error('Empty content for post: %s' % p.link)	
					self._monitor.content_exception(provider, p.link, Exception('Empty content'))
					self._yandex_queue.put(p)

			except Errors.HttpError as e:
				self.logger.error('Http error code %s on url %s' % (e.code, e.url))
				self._monitor.content_http_error(provider, e.code, e.url)
				self._yandex_queue.put(p)
		
			except Exception as e:
				self.logger.exception(e)
				self._monitor.content_exception(provider, p.link, e)
				self._yandex_queue.put(p)


	def on_start(self, connection):
		super(Runner, self).on_start(connection)

		self._monitor_queue = MQ.BaseQueue(connection, Consts.Queues.MONITOR, self.name)
		self._monitor = MonSender.Sender(self._monitor_queue)

		self._yandex_queue = MQ.BaseQueue(connection, Consts.Queues.POSTS_4_CONTENT_COLLECT_YA, self.name)

		self._readers = {
			Consts.Providers.LJ : LJ.ContentReader(self.name, self._monitor),
			Consts.Providers.VK : VK.ContentReader(self.name, self._monitor),
			Consts.Providers.BLOGSPOT : Blogspot.ContentReader(self.name, self._monitor),
			Consts.Providers.YA_BLOG : YaBlog.ContentReader(self.name, self._monitor)
		}

		
	def on_finish(self):
		self._monitor_queue.close()
		self._yandex_queue.close()

		super(Runner, self).on_finish()


