#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SearchDB

class Repository(object):

	def __init__(self, session):
		self.session = session

	def add_post(self, p):
		blog_host = self.get_blog_host_by_name(p.host)
		if blog_host is None:
			blog_host = self.add_blog_host(p.host)

		author = self.get_author_by_name(p.author)
		if author is None:
			author = self.add_author(p.author)

		post = SearchDB.Post(title = p.title, 
			link = p.link, 
			publish_date = p.publish_date,
			collected_date = p.collected,
			query_id = p.query_id,
			author_id = author.id,
			blog_host_id = blog_host.id)

		self.session.add(post)
		self.session.commit()

		content = SearchDB.PostContent(post_id = post.id, content = p.content)
		self.session.add(content)
		self.session.commit()

		return self.session.query(SearchDB.Post).filter_by(id=post.id).one()

	def get_posts_by_query(self, query_id):
		return self.session.query(SearchDB.Post).filter_by(query_id=query_id).all()

	def get_post_by_id(self, id):
		return self.session.query(SearchDB.Post).filter_by(id=id).first()
		
	def get_post_content_by_post_id(self, post_id):
		return self.session.query(SearchDB.PostContent).filter_by(post_id=post_id).one()

	
	def add_author(self, blog):
		author = SearchDB.Author(blog = blog)
		self.session.add(author)
		self.session.commit()
		return author

	def get_authors(self):
		return self.session.query(SearchDB.Author).all()
	
	def get_author_by_id(self, id):
		return self.session.query(SearchDB.Author).filter_by(id=id).first()

	def get_author_by_name(self, name):
		return self.session.query(SearchDB.Author).filter_by(blog=name).first()

	
	def add_blog_host(self, host):
		blog_host = SearchDB.BlogHost(host = host)
		self.session.add(blog_host)
		self.session.commit()
		return blog_host

	def get_blog_hosts(self):
		return self.session.query(SearchDB.BlogHost).all()

	def get_blog_host_by_id(self, id):
		return self.session.query(SearchDB.BlogHost).filter_by(id=id).first()

	def get_blog_host_by_name(self, name):
		return self.session.query(SearchDB.BlogHost).filter_by(host=name).first()