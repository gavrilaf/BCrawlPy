
class Runners(object):
	SEARCH_CONTROLLER = 'controller'
	YANDEX_SEARCHER = 'yandex-searcher'
	FILTER = 'filter'
	YA_CONTENT_COLLECTOR = 'ya-content-collector'
	LJ_CONTENT_COLLECTOR = 'lj-content-collector'
	VK_CONTENT_COLLECTOR = 'vk-content-collector'
	PERSISTER = 'persister'
	MONITOR = 'monitor'

	TEST = 'test'

class Queues(object):
	QUERIES = 'MQ_Queries4Search'
	POSTS_4_FILTER = 'MQ_Posts4Filter'
	POSTS_4_CONTENT_COLLECT_YA = 'MQ_Posts4Collect_Ya'
	POSTS_4_CONTENT_COLLECT_LJ = 'MQ_Posts4Collect_Lj'
	POSTS_4_CONTENT_COLLECT_VK = 'MQ_Posts4Collect_Vk'
	POSTS_4_PERSIST = 'MQ_Posts4Persist'
	QUERY_STATUSES = 'MQ_QueryStatuses'
	MONITOR = 'MQ_Monitor'
	

class Providers(object):
	YANDEX = 1
	TWITTER = 2
	LJ = 3
	VK = 4