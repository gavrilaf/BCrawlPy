#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Runners(object):
	SEARCH_CONTROLLER = 'controller'
	YANDEX_SEARCHER = 'yandex-searcher'
	ROUTER = 'router'
	YANDEX_CONTENT_COLLECTOR = 'ya-content-collector'
	COMMON_CONTENT_COLLECTOR = 'common-content-collector'	
	PERSISTER = 'persister'
	MONITOR = 'monitor'
	REPORTER = 'reporter'

	TEST = 'test'

class Queues(object):
	QUERIES = 'MQ_Queries4Search'
	POSTS_4_ROUTE = 'MQ_Posts4Filter'
	POSTS_4_CONTENT_COLLECT_YA = 'MQ_Posts4Collect_Ya'
	POSTS_4_CONTENT_COLLECT_COMMON = 'MQ_Posts4Collect_Common'
	POSTS_4_PERSIST = 'MQ_Posts4Persist'
	QUERY_STATUSES = 'MQ_QueryStatuses'
	MONITOR = 'MQ_Monitor'
	
class Providers(object):
	YANDEX = 1
	TWITTER = 2
	LJ = 3
	VK = 4
	YA_BLOGS = 5
	LI = 6
	BLOGSPOT = 7