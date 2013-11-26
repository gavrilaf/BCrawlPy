#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
from bcrawl.search import YaSearch

if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = YaSearch.Runner()
	p.run()
