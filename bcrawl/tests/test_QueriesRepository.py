import unittest
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bcrawl.base import Consts
from bcrawl.base import DB
from bcrawl.runners import Queries
from bcrawl.runners import SearchDB


class QueriesRepositoryTests(unittest.TestCase):

	def setUp(self):
		self.engine = create_engine('sqlite:///:memory:')
		DB.Base.metadata.create_all(self.engine)
		Session = sessionmaker(bind=self.engine)
		self.session = Session()
		self.rep = Queries.Repository(self.session)

	def tearDown(self):
		self.session.close()

	def test_SearchObjects(self):
		self.assertEqual(len(self.rep.get_sobjects()), 0)

		sobj = self.rep.add_sobject('test')
		self.assertIsNotNone(sobj)

		self.assertEqual(sobj.name, self.rep.get_sobject_by_id(sobj.id).name)

		objs = self.rep.get_sobjects()

		self.assertEqual(len(objs), 1)
		self.assertEqual(objs[0].id, sobj.id)

	def test_Queries(self):
		sobj = self.rep.add_sobject('test')
		start_day = datetime.date(2013, 10, 20)

		query = self.rep.add_query(sobj.id, Consts.Providers.YANDEX, 'test-q', start_day)
		self.assertIsNotNone(query)

		lst1 = self.rep.get_queries_by_sobject(sobj.id)
		lst2 = self.rep.get_queries_by_provider(Consts.Providers.YANDEX)

		self.assertEqual(len(lst1), 1)
		self.assertEqual(len(lst2), 1)

		self.assertEqual(lst1[0].id, sobj.id)
		self.assertEqual(lst1[0].provider, Consts.Providers.YANDEX)
		self.assertEqual(lst1[0].text, 'test-q')
		self.assertEqual(lst1[0].start_from, start_day)

		self.assertEqual(lst2[0].id, sobj.id)
		self.assertEqual(lst2[0].provider, Consts.Providers.YANDEX)
		self.assertEqual(lst2[0].text, 'test-q')
		self.assertEqual(lst2[0].start_from, start_day)

	def test_DayQueries(self):
		sobj = self.rep.add_sobject('test')
		query = self.rep.add_query(sobj.id, Consts.Providers.YANDEX, 'test-q', datetime.date(2013, 10, 20))

		day1 = self.rep.add_day_query(query.id, datetime.date(2013, 10, 20))
		day2 = self.rep.add_day_query(query.id, datetime.date(2013, 10, 21))

		self.assertIsNotNone(day1)
		self.assertIsNotNone(day2)

		days = self.rep.get_day_queries(query.id)

		self.assertEqual(len(days), 2)
		self.assertEqual(days[0].day, datetime.date(2013, 10, 20))
		self.assertEqual(days[1].day, datetime.date(2013, 10, 21))

		days = self.rep.get_day_queries_with_status(query.id, SearchDB.DayQuery.STATUS_COMPLETED)
		self.assertEqual(len(days), 0)

		self.rep.update_day_query_status(day1.id, SearchDB.DayQuery.STATUS_COMPLETED)

		days = self.rep.get_day_queries_with_status(query.id, SearchDB.DayQuery.STATUS_NEW)
		self.assertEqual(len(days), 1)

		days = self.rep.get_day_queries_with_status(query.id, SearchDB.DayQuery.STATUS_COMPLETED)
		self.assertEqual(len(days), 1)

		days = self.rep.get_day_queries_with_status(query.id, SearchDB.DayQuery.STATUS_IN_PROGRESS)
		self.assertEqual(len(days), 0)