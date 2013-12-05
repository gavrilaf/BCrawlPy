import logging

def config_logger(runner_name):

	logger = logging.getLogger(runner_name)
	logger.setLevel(logging.DEBUG)

	# create formatter
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

	# create console handler 
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	ch.setFormatter(formatter)

	# create file handler
	fh = logging.FileHandler('logs/'+runner_name+'.log')
	fh.setLevel(logging.DEBUG)
	fh.setFormatter(formatter)

	# add handlers to logger
	logger.addHandler(ch)
	logger.addHandler(fh)