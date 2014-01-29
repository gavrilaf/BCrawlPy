#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from bcrawl.db import Queries, SearchDB


_REPORT_NAME = "QueriesStatus"

class Generator(object):
	def __init__(self, session):
		self.search_db = Queries.Repository(session)

	@property
	def name(self):
		return _REPORT_NAME

	def calculate(self):
		result = {'objects' : []}

		objs = self.search_db.get_sobjects()
		for obj in objs:
			obj_rep = {'name' : obj.name, 'progress' : 0, 'queries' : []}

			obj_day_query_total = 0
			obj_day_query_completed = 0

			for query in obj.queries:
				in_progress = []
				completed_count = 0

				for day_query in query.day_queries:

					if day_query.status == SearchDB.DayQuery.STATUS_IN_PROGRESS:
						in_progress.append(str(day_query.day))
					elif day_query.status == SearchDB.DayQuery.STATUS_COMPLETED:
						completed_count += 1

				total = len(query.day_queries)

				query_rep = {
					'text' : query.text, 
					'total' : total, 
					'in_progress' : len(in_progress),
					'completed' : completed_count,
					'in_progress_lst' : ', '.join(in_progress),
					'progress' :  ( 100 * completed_count ) / total if total != 0 else 0
				}

				obj_day_query_total += total
				obj_day_query_completed += completed_count

				obj_rep['queries'].append(query_rep)

			obj_rep['progress'] = ( 100 * obj_day_query_completed ) / obj_day_query_total if obj_day_query_total != 0 else 0

			result['objects'].append(obj_rep)

		return result


class Report(object):
	
	def get_report(self, reports_db):
		collection = reports_db[_REPORT_NAME]
		report = collection.find_one()
		
		if report is None: # create empty
			return {'timestamp' : 'Report not found', 'content' : {'objects' : []} }
		
		return {'timestamp' : report['timestamp'].strftime('%d.%m.%Y %H:%M:%S'), 'content' : report['content'] }

		


