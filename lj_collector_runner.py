#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import Log, Consts
from bcrawl.content import LjCollector

if __name__ == '__main__':
	Log.config_logger(Consts.Runners.LJ_CONTENT_COLLECTOR)
	p = LjCollector.Runner()
	p.run()
