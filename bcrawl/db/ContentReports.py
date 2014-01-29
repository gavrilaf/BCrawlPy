#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SearchDB import *
from sqlalchemy import desc

class Repository(object):

	def __init__(self, session):
		self.session = session

	def get_top_posts(self, limit):
		return self.session.query(Post, Query, SObject, Author, BlogHost, PostContent) \
			.join(Query) \
			.join(SObject) \
			.join(Author) \
			.join(BlogHost) \
			.join(PostContent) \
			.order_by(desc(Post.collected_date)) \
			.limit(limit) \
			.all()