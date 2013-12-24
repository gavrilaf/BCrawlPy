import unittest
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bcrawl.base import Consts
from bcrawl.db import DB, SearchDB, Queries


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

		query = self.rep.add_query(sobj.id, 'test-q', start_day)
		self.assertIsNotNone(query)

		lst1 = self.rep.get_queries_by_sobject(sobj.id)
		lst2 = self.rep.get_all_queries()
	
		self.assertEqual(len(lst1), 1)
		self.assertEqual(len(lst2), 1)
		
		self.assertEqual(lst1[0].id, sobj.id)
		self.assertEqual(lst1[0].text, 'test-q')
		self.assertEqual(lst1[0].start_from, start_day)

		self.assertEqual(lst2[0].id, sobj.id)
		self.assertEqual(lst2[0].text, 'test-q')
		self.assertEqual(lst2[0].start_from, start_day)


	def test_DayQueries(self):
		sobj = self.rep.add_sobject('test')
		query = self.rep.add_query(sobj.id, 'test-q', datetime.date(2013, 10, 20))

		day1 = self.rep.add_day_query(query.id, datetime.date(2013, 10, 20))
		day2 = self.rep.add_day_query(query.id, datetime.date(2013, 10, 21))

		self.assertIsNotNone(day1)
		self.assertIsNotNone(day2)

		days = self.rep.get_day_queries(query.id)

		self.assertEqual(len(days), 2)
		self.assertEqual(days[0].day, datetime.date(2013, 10, 20))
		self.assertEqual(days[1].day, datetime.date(2013, 10, 21))

		# Check backref
		self.assertEqual(days[0].query.id, query.id)
		self.assertEqual(days[0].query.text, query.text)

		days = self.rep.get_day_queries_with_status(query.id, SearchDB.DayQuery.STATUS_COMPLETED) # All day queries have status NEW
		self.assertEqual(len(days), 0)

		self.rep.update_day_query_status(day1.id, SearchDB.DayQuery.STATUS_COMPLETED)

		days = self.rep.get_day_queries(query.id)
		self.assertEqual(len(days), 2) # Day query must be updated (not created)

		days = self.rep.get_day_queries_with_status(query.id, SearchDB.DayQuery.STATUS_NEW)
		self.assertEqual(len(days), 1)
		self.assertEqual(days[0].day, day2.day)

		days = self.rep.get_day_queries_with_status(query.id, SearchDB.DayQuery.STATUS_COMPLETED)
		self.assertEqual(len(days), 1)
		self.assertEqual(days[0].day, day1.day)

		days = self.rep.get_day_queries_with_status(query.id, SearchDB.DayQuery.STATUS_IN_PROGRESS)
		self.assertEqual(len(days), 0)

	def test_QueryEx(self):
		o1 = self.rep.add_sobject('test')
		q1 = self.rep.add_query(o1.id, 'test-q', datetime.date.today()-datetime.timedelta(2))

		q2 = self.rep.get_query_by_id(q1.id)

		lst = q2.get_days_to_now()

		self.assertEqual(len(lst), 3)
		self.assertEqual(lst[0], q2.start_from)
		self.assertEqual(lst[1], q2.start_from+datetime.timedelta(1))
		self.assertEqual(lst[2], datetime.date.today())

		# Add first day
		self.rep.add_day_query(q2.id, lst[0])

		q2 = self.rep.get_query_by_id(q1.id)
		lst = q2.get_days_to_now()

		self.assertEqual(len(lst), 2)
		self.assertEqual(lst[0], q2.start_from+datetime.timedelta(1))
		self.assertEqual(lst[1], datetime.date.today())

		# Add second day
		self.rep.add_day_query(q2.id, lst[0])

		q2 = self.rep.get_query_by_id(q1.id)
		lst = q2.get_days_to_now()

		self.assertEqual(len(lst), 1)
		self.assertEqual(lst[0], datetime.date.today())

		# Add third day
		self.rep.add_day_query(q2.id, lst[0])

		q2 = self.rep.get_query_by_id(q1.id)
		lst = q2.get_days_to_now()

		self.assertEqual(len(lst), 0)
		

