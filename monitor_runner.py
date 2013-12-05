#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import Log, Consts
from bcrawl.monitor import Monitor

if __name__ == '__main__':
	Log.config_logger(Consts.Runners.MONITOR)
	p = Monitor.Runner()
	p.run()
