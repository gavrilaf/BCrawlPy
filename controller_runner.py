#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
from bcrawl.controller import Controller

if __name__ == '__main__':
	logging.config.fileConfig("logging.conf")
	p = Controller.Runner()
	p.run()
	



