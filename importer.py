#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from dateutil import parser
from contextlib import closing
from bcrawl.base import Consts, DB
from bcrawl.runners import Queries

if __name__ == '__main__':

	with closing(open('bcrawl-queries.json', 'r')) as fp:
		with closing(DB.Context('sqlite:///data/search.db')) as context:
			data = json.load(fp)
			db = Queries.Repository(context.session)

			for obj in data['data']:
				sobj = db.add_sobject(obj['sobject'])
				print unicode(sobj)

				for query in obj['queries']:
					pq = db.add_query(sobj.id, Consts.Providers.YANDEX, query['text'], parser.parse(query['start_date']))	
					print unicode(pq)
			
				print "-------------------------\n"
		
		