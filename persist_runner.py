import logging.config
from bcrawl.runners import Persister

if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = Persister.PostPersister('sqlite:///data/search.db')
	p.run()
