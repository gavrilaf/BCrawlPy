#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import Log, Consts
from bcrawl.content import YaCollector

if __name__ == '__main__':
	Log.config_logger(Consts.Runners.YA_CONTENT_COLLECTOR)
	p = YaCollector.Runner()
	p.run()
