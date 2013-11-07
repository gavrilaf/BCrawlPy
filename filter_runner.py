import logging.config
from bcrawl.runners import Filter

if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = Filter.Producer()
	p.run()
