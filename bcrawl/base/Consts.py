#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Runners(object):
	SEARCH_CONTROLLER = 'controller'
	YANDEX_SEARCHER = 'yandex-searcher'
	ROUTER = 'router'
	YA_CONTENT_COLLECTOR = 'ya-content-collector'
	LJ_CONTENT_COLLECTOR = 'lj-content-collector'
	VK_CONTENT_COLLECTOR = 'vk-content-collector'
	PERSISTER = 'persister'
	MONITOR = 'monitor'
	REPORTER = 'reporter'

	TEST = 'test'

class Queues(object):
	QUERIES = 'MQ_Queries4Search'
	POSTS_4_ROUTE = 'MQ_Posts4Filter'
	POSTS_4_CONTENT_COLLECT_YA = 'MQ_Posts4Collect_Ya'
	POSTS_4_CONTENT_COLLECT_LJ = 'MQ_Posts4Collect_Lj'
	POSTS_4_CONTENT_COLLECT_VK = 'MQ_Posts4Collect_Vk'
	POSTS_4_PERSIST = 'MQ_Posts4Persist'
	QUERY_STATUSES = 'MQ_QueryStatuses'
	MONITOR = 'MQ_Monitor'
	POST_ERRORS = 'MQ_PostsErrors'
	

class Providers(object):
	YANDEX = 1
	TWITTER = 2
	LJ = 3
	VK = 4