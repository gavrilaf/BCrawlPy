from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Context(object):

	def __init__(self, db_path):
		_engine = create_engine(db_path)
		
		Base.metadata.create_all(_engine)
		Session = sessionmaker(bind=_engine)

		self.session = Session()

	def close(self):
		self.session.close()



