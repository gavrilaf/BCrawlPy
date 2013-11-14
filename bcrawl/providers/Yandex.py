#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import logging
import xml.dom.minidom

from bcrawl.base import MQData


def element_value(root, tag):
	try:
		return root.getElementsByTagName(tag)[0].firstChild.nodeValue
	except Exception as e:
		raise XmlTagError(tag, e) 

def element_attr_value(root, tag, attr):
	try:
		return root.getElementsByTagName(name)[0].getAttribute(attr).nodeValue
	except Exception as e:
		raise XmlTagError(tag+'::'+attr, e) 


class Searcher(object):
	DEF_NUMDOC = 100

	def __init__(self, runner_name, monitor, numdoc = DEF_NUMDOC):
		self.logger = logging.getLogger(runner_name)
		self.monitor = monitor

		self.query = ''
		self.numdoc = numdoc

		self.yandex_count = 0

	def start_search(self, query):
		self.query = query

		self.finished = False
		self.page = 0

		return self.send_request()

	def next(self):
		if self.finished:
			return []

		return self.send_request()

	def send_request(self):
		p = {
			u'text': self.query.text, 
			'ft' : 'blog', 
			'numdoc' : self.numdoc, 
			'from_day' : self.query.day.day, 'from_month' : self.query.day.month, 'from_year' : self.query.day.year,
			'to_day' : self.query.day.day, 'to_month' : self.query.day.month, 'to_year' : self.query.day.year}

		if self.page != 0:
			p['p'] = self.page
		
		r = requests.get("http://blogs.yandex.ru/search.rss", params=p)

		self.monitor.search_http_request(MQData.PROVIDER_YANDEX, self.query.query_id)  # Notify monitor about http request
		self.logger.info('Searcher: (%s, %d)' % (r.url, r.status_code))
		
		if r.status_code != 200:
			raise HttpError(r)
		
		self.page += 1
		posts =  self.parse_response(r)

		if len(posts) < self.numdoc:
			self.finished = True

		return posts

	def parse_response(self, r):
		xmldoc = xml.dom.minidom.parseString(r.text.encode('utf-8'))

		self.yandex_count = element_value(xmldoc, 'yablogs:count')
	
		posts = []
		items = xmldoc.getElementsByTagName('item')

		for item in items:
			post = self.parse_item(item)
			if post is not None:
				posts.append(post)

		return posts

	def parse_item(self, item):
		fields = ['link', 'title', 'pubDate', 'author']
		values = []

		for field in fields: 
			try:
				if field == 'author':
					values.append(self.parse_author(item))
				else:
					values.append(element_value(item, field))
			except XmlTagError as e:
				if field == 'link':
					self.logger.warning('Yandex.Searcher: post without link!')
					return None
				self.log.warning('Yandex.Searcher: tag %s not found for post %s' % (e.tag, values[0]))
				values.append('')

		return MQData.Post.from_values(self.query.query_id, MQData.PROVIDER_YANDEX, values)

	def parse_author(self, item):
		e = item.getElementsByTagName('author')
		if len(e) == 1:
			return e[0].firstChild.nodeValue

		e = item.getElementsByTagName('yablogs:journal')
		if len(e) == 1:
			return e[0].getAttribute('url')

		e = item.getElementsByTagName('yablogs:journal')
		if len(e) == 1:
			return e[0].getAttribute('url')

		raise XmlTagError('author')



class SearchBroker(object):

	def __init__(self, runner_name, monitor):
		self.logger = logging.getLogger(runner_name)
		self.monitor = monitor
		self.searcher = Searcher(runner_name, monitor)

	def read_day_posts(self, query, out_queue):
		self.logger.info("Broker got query: %s" % query)

		total_count = 0

		posts = self.searcher.start_search(query)
		self.logger.info('Yandex count = %s' % self.searcher.yandex_count)

		posts_count = len(posts)
		while posts_count > 0:
			total_count += posts_count
				
			for p in posts:
				out_queue.put(p) 
				self.monitor.post_collected(p.link)

			self.logger.info('%s: collected %d posts' % (str(query.day), posts_count))

			posts = self.searcher.next()
			posts_count = len(posts)
			
		self.logger.info('%s: Total collected %d posts' % (str(query.day), total_count))


class ContentReader(object):
	def __init__(self, runner_name, monitor):
		self.logger = logging.getLogger(runner_name)
		self.monitor = monitor

	def read_content(self, url):
		p = {
			'text': 'url="'+url+'"', 
			'full' : '1'}

		r = requests.get("http://blogs.yandex.ru/search.rss", params=p)

		self.monitor.search_http_request(MQData.PROVIDER_YANDEX, None)  # Notify monitor about http request
		self.logger.info('Yandex.ContentReader: (%s, %d)' % (r.url, r.status_code))

		if r.status_code != 200:
			raise HttpError(r)

		return self.parse_response(r)

	def parse_response(self, r):
		xmldoc = xml.dom.minidom.parseString(r.text.encode('utf-8'))
		items = xmldoc.getElementsByTagName('item')
		if len(items) == 0:
			return None

		txt = element_value(items[0], 'description')
		self.logger.debug('Content: %s' % txt)

		return txt
