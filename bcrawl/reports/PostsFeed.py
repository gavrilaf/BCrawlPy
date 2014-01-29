#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
import datetime
from dateutil.tz import *
import pytz
from bcrawl.db import ContentReports

_REPORT_NAME = "PostsFeed"

def unaware_utc_to_local(utc_dt):
	utctz = pytz.UTC
	utc_dt = utctz.localize(utc_dt)

	localtz = pytz.timezone(tzlocal().tzname(datetime.datetime.now()))
	return localtz.normalize(utc_dt.astimezone(localtz))

def pretty_datetime(dt):
	return dt.strftime("%d.%m.%Y %H:%M:%S")


def smart_truncate(text, max_length=100, suffix='...'):
    """Returns a string of at most `max_length` characters, cutting
    only at word-boundaries. If the string was truncated, `suffix`
    will be appended.
    """

    if len(text) > max_length:
        #pattern = r'^(.{0,%d}\S)\s.*' % (max_length-len(suffix)-1)
        #return re.sub(pattern, r'\1' + suffix, text)
        return text[:max_length].rsplit(' ', 1)[0]+suffix
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
				'published' : pretty_datetime(unaware_utc_to_local(post.Post.publish_date)),
				'collected' : pretty_datetime(unaware_utc_to_local(post.Post.collected_date)),
				'content' : smart_truncate(content, 500, '...'),
				'bloghost' : post.BlogHost.host,
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


