#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import Log, Consts
from bcrawl.content import CommonCollector

if __name__ == '__main__':
	Log.config_logger(Consts.Runners.COMMON_CONTENT_COLLECTOR)
	p = CommonCollector.Runner()
	p.run()

	