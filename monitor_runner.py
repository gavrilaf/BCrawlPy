import logging.config
from bcrawl.monitor import Monitor

if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = Monitor.Runner()
	p.run()
