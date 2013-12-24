import unittest
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bcrawl.base import Consts
from bcrawl.db import DB, ContentReports, SearchDB



class QueriesRepositoryTests(unittest.TestCase):

	def setUp(self):
		self.engine = create_engine('sqlite:///:memory:')
		DB.Base.metadata.create_all(self.engine)
		Session = sessionmaker(bind=self.engine)
		self.session = Session()
		self.rep = Queries.Repository(self.session)



	def tearDown(self):
		self.session.close()

