#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import Log, Consts
from bcrawl.search import YaSearch

if __name__ == '__main__':
	Log.config_logger(Consts.Runners.YANDEX_SEARCHER)
	p = YaSearch.Runner()
	p.run()
