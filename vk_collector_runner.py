import logging.config
from bcrawl.content import VkCollector

if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = VkCollector.Runner()
	p.run()

	