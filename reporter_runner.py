#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
from bcrawl.reports import Reporter

if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = Reporter.Runner('sqlite:///data/search.db', 'bcrawl-reports')
	p.run()