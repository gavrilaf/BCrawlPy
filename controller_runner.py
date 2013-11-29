#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
from bcrawl.runners import Controller

if __name__ == '__main__':
	logging.config.fileConfig('logging.conf')
	p = Controller.Runner('sqlite:///data/search.db')
	p.run()
	



