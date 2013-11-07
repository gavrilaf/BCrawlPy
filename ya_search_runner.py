#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
from bcrawl.runners import YaSearch

if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = YaSearch.Producer()
	p.run()
