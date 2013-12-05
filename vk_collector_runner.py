#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import Log, Consts
from bcrawl.content import VkCollector

if __name__ == '__main__':
	Log.config_logger(Consts.Runners.VK_CONTENT_COLLECTOR)
	p = VkCollector.Runner()
	p.run()

	