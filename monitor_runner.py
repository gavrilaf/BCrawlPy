import logging.config
from bcrawl.runners import Monitor

if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = Monitor.Consumer()
	p.run()
