#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SearchDB

class Repository(object):

	def __init__(self, session):
		self.session = session

	def add_sobject(self, name):
		obj = SearchDB.SObject(name)
		self.session.add(obj)
		self.session.commit()
		return obj

	def get_sobjects(self):
		return self.session.query(SearchDB.SObject).all()

	def get_sobject_by_id(self, id):
		return self.session.query(SearchDB.SObject).filter_by(id=id).one()

	def add_query(self, sobj_id, text, start_day):
		query = SearchDB.Query(sobj_id, text, start_day)
		self.session.add(query)
		self.session.commit()
		return query

	def get_query_by_id(self, query_id):
		return self.session.query(SearchDB.Query).filter_by(id=query_id).one()

	def get_all_queries(self):
		return self.session.query(SearchDB.Query).all()

	def get_queries_by_sobject(self, sobj_id):
		return self.session.query(SearchDB.Query).filter_by(sobject_id=sobj_id).all()

	def add_day_query(self, query_id, day):
		day_query = SearchDB.DayQuery(query_id = query_id, day = day, status = SearchDB.DayQuery.STATUS_NEW)
		self.session.add(day_query)
		self.session.commit()
		return day_query

	def get_day_query_by_id(self, day_query_id):
		return self.session.query(SearchDB.DayQuery).filter_by(id=day_query_id).one()

	def get_day_queries(self, query_id):
		return self.session.query(SearchDB.DayQuery).filter_by(query_id=query_id).order_by("day").all()

	def get_all_day_queries_with_status(self, status):
		return self.session.query(SearchDB.DayQuery).filter_by(status=status).order_by("day").all()

	def get_day_queries_with_status(self, query_id, status):
		return self.session.query(SearchDB.DayQuery).filter_by(query_id=query_id, status=status).order_by("day").all()

	def update_day_query_status(self, day_query_id, new_status):
		day = self.session.query(SearchDB.DayQuery).filter_by(id=day_query_id).one()
		day.status = new_status
		self.session.merge(day)
		self.session.commit()
		
		