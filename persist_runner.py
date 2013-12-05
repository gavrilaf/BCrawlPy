#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bcrawl.base import Log, Consts
from bcrawl.runners import Persister

if __name__ == '__main__':
	Log.config_logger(Consts.Runners.PERSISTER)
	p = Persister.PostPersister('sqlite:///data/search.db')
	p.run()
