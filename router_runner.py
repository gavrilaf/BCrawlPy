#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import Log, Consts
from bcrawl.router import Router

if __name__ == '__main__':
	Log.config_logger(Consts.Runners.ROUTER)
	p = Router.Runner()
	p.run()
