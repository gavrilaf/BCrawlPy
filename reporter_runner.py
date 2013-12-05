#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import Log, Consts
from bcrawl.reports import Reporter

if __name__ == '__main__':
	Log.config_logger(Consts.Runners.REPORTER)
	p = Reporter.Runner('sqlite:///data/search.db', 'bcrawl-reports')
	p.run()