#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SearchDB import *

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
			.order_by(Post.collected_date) \
			.limit(limit)