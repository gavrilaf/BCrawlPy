#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from bcrawl.runners import SearchDB

_REPORT_NAME = "PostsTotal"

class Generator(object):
	def __init__(self, search_db):
		self.search_db = search_db

	@property
	def name(self):
		return _REPORT_NAME

	def calculate(self):
		result = {'objects' : []}

		objs = self.search_db.get_sobjects()
		
		for obj in objs:
			obj_rep = {'name' : obj.name, 'posts_total' : 0, 'queries' : []}

			posts_total = 0
			for query in obj.queries:
				posts_count = len(query.posts)
				posts_total += posts_count
				
				query_rep = {
					'text' : query.text, 
					'posts_total' : posts_count
				}
				obj_rep['queries'].append(query_rep)

			obj_rep['posts_total'] = posts_total

			result['objects'].append(obj_rep)

		return result


class Report(object):
	
	def get_report(self, reports_db):
		collection = reports_db[_REPORT_NAME]
		report = collection.find_one()
		if report:
			return {'timestamp' : report['timestamp'].strftime('%d.%m.%Y %H:%M:%S'), 'content' : report['content'] }

		return None


