#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
from bcrawl.db import ContentReports

_REPORT_NAME = "PostsFeed"

def smart_truncate(text, max_length=100, suffix='...'):
    """Returns a string of at most `max_length` characters, cutting
    only at word-boundaries. If the string was truncated, `suffix`
    will be appended.
    """

    if len(text) > max_length:
        pattern = r'^(.{0,%d}\S)\s.*' % (max_length-len(suffix)-1)
        return re.sub(pattern, r'\1' + suffix, text)
    else:
        return text

class Generator(object):
	def __init__(self, session):
		self.repository = ContentReports.Repository(session)

	@property
	def name(self):
		return _REPORT_NAME

	def calculate(self):
		result = {'posts' : []}

		posts = self.repository.get_top_posts(20)
		for post in posts:
			content = post.PostContent.content
			if content is None:
				content = post.Post.title
			jrep = {
				'title' : post.Post.title,
				'link' : post.Post.link,
				'published' : post.Post.publish_date,
				'collected' : post.Post.collected_date,
				'content' : smart_truncate(content, 200, '...'),
				'bloghot' : post.BlogHost.host,
				'author' : post.Author.blog,
				'object' : post.SObject.name
			}

			result['posts'].append(jrep)
		
		return result


class Report(object):
	
	def get_report(self, reports_db):
		collection = reports_db[_REPORT_NAME]
		report = collection.find_one()
		if report:
			return {'timestamp' : report['timestamp'].strftime('%d.%m.%Y %H:%M:%S'), 'content' : report['content'] }

		return None


