from bcrawl.base import MQ, Consts, Log
from bcrawl.router import BlogHost

_RUNNER_NAME = 'BLOGHOST_STAT_RUNNER'

class Runner(MQ.BaseConsumer):
	def __init__(self, in_queue_name):
		super(Runner, self).__init__(in_queue_name, _RUNNER_NAME)				
	
	def process(self, p):
		host = self._detector.get_blog_host(p.link)
		self.logger.info(host)

		if host in self._hosts:
			self._hosts[host] +=1
		else:
			self._hosts[host] = 1
		
	def on_start(self, connection):
		super(Runner, self).on_start(connection)

		self._detector = BlogHost.Detector()
		self._hosts = {}

	def on_finish(self):
		super(Runner, self).on_finish()

		self.logger.info(str(self._host))


if __name__ == '__main__':
	Log.config_logger(_RUNNER_NAME)
	p = Runner(Consts.Queues.POSTS_4_CONTENT_COLLECT_YA)
	p.run()

		

	