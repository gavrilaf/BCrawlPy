import unittest
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bcrawl.base import Consts, MQData
from bcrawl.db import DB, ContentReports, SearchDB, Queries, Posts



class QueriesRepositoryTests(unittest.TestCase):

	def setUp(self):
		self.engine = create_engine('sqlite:///:memory:')
		DB.Base.metadata.create_all(self.engine)
		Session = sessionmaker(bind=self.engine)
		self.session = Session()
		
		self.queries_rep = Queries.Repository(self.session)
		self.posts_rep = Posts.Repository(self.session)
		self.reports_rep = ContentReports.Repository(self.session)

	def tearDown(self):
		self.session.close()


	def test_Top10Report(self):
		sobj = self.queries_rep.add_sobject('test')
		query = self.queries_rep.add_query(sobj.id, 'test-q', datetime.date(2013, 10, 20))

		for i in range(20):
			d2 = datetime.datetime.utcnow().replace(microsecond=0)
			d1 = d2 - datetime.timedelta(days=5)

			p = MQData.Post(query_id = 1, 
				provider = Consts.Providers.YANDEX,
				title = 'test title',
				link = 'test link' + str(i),
				publish_date = d1,
				author = 'test author')

			p.host = 'test host'
			p.content = 'test content'
			
			self.posts_rep.add_post(p)

		posts = self.reports_rep.get_top_posts(10)
		self.assertIsNotNone(posts)
		self.assertEqual(len(posts), 10)

		posts = self.reports_rep.get_top_posts(19)
		self.assertIsNotNone(posts)
		self.assertEqual(len(posts), 19)

		posts = self.reports_rep.get_top_posts(2)
		self.assertIsNotNone(posts)
		self.assertEqual(len(posts), 2)

		
