import logging.config
from bcrawl.content import YaCollector

if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = YaCollector.Runner()
	p.run()
