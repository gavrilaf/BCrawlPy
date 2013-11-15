import logging.config
from bcrawl.runners import Router

if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = Router.Runner()
	p.run()
