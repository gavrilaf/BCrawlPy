import logging.config
from bcrawl.runners import Monitor

#from bcrawl.db import Monitor

if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = Monitor.Consumer()
	p.run()

	#rep = Monitor.Repository()
	#status = rep.status_full()
	#print status
