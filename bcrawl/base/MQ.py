import kombu
import time
import logging
import jsonpickle
from contextlib import closing

class BaseLoggedObj(object):
	def __init__(self, name):
		self.name_ = name
		self.logger_ = logging.getLogger(name)

	@property
	def name(self):
		return self.name_

	@property
	def logger(self):
		return self.logger_	


class BaseQueue(BaseLoggedObj):
	def __init__(self, conn, queue_name, runner_name):
		super(BaseQueue, self).__init__(runner_name)
		
		self.queue_name = queue_name
		self.queue = conn.SimpleQueue(queue_name)
		self.msg = None

	def get(self):
		try:
			self.msg = self.queue.get(block=True, timeout=1)
			obj = jsonpickle.decode(self.msg.payload)
			return obj
		except:
			# TODO: Add correct exception handling
			return None

	def put(self, obj):
		self.queue.put(jsonpickle.encode(obj))

	def ack(self):
		if self.msg is not None:
			self.msg.ack()

	def close(self):
		self.logger.info('Queue %s closed' % self.queue_name)
		self.queue.close()

class BaseConsumer(BaseLoggedObj):
	def __init__(self, queue_name, runner_name):
		super(BaseConsumer, self).__init__(runner_name)
		self.queue_name = queue_name

		
	def run(self):
		with kombu.Connection() as conn:
			self.on_start(conn)
			with closing(BaseQueue(conn, self.queue_name, self.name)) as queue:
				try:
					while True: # TODO: Add correct way to exit run loop
						obj = queue.get()
						if obj is not None:
							self.process(obj)
							queue.ack()
						else:
							time.sleep(1)
				finally:
					self.on_finish()
				

	def on_start(self, connection):
		self.logger.info(self.name + ' is started')
		
	def on_finish(self):
		self.logger.info(self.name + ' is finished')

	def process(self, p):
		raise NotImplementedError("Should have implemented this") 


class BaseProducer(BaseLoggedObj):
	def __init__(self, in_queue_name, out_queue_name, runner_name):
		super(BaseProducer, self).__init__(runner_name)
		self.in_queue_name = in_queue_name
		self.out_queue_name = out_queue_name

	
	def run(self):
		with kombu.Connection() as conn:
			self.on_start(conn)
			with closing(BaseQueue(conn, self.in_queue_name, self.name)) as in_queue: 
				with closing(BaseQueue(conn, self.out_queue_name, self.name)) as out_queue:
					try:
						while True: # TODO: Add correct way to exit run loop
							obj = in_queue.get()
							if obj is not None:
								self.process(obj, out_queue)
								in_queue.ack()
							else:
								time.sleep(1)
					finally:
						self.on_finish()

	def on_start(self, connection):
		self.logger.info(self.name + ' is started')

	def on_finish(self):
		self.logger.info(self.name + ' is finished')

	def process(self, p, out_queue):
		raise NotImplementedError("Should have implemented this") 





		


