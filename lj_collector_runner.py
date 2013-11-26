import logging.config
from bcrawl.content import LjCollector

if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = LjCollector.Runner()
	p.run()
