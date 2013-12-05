#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import Log, Consts
from bcrawl.runners import Controller

if __name__ == '__main__':
	Log.config_logger(Consts.Runners.SEARCH_CONTROLLER)
	p = Controller.Runner('sqlite:///data/search.db')
	p.run()
	



