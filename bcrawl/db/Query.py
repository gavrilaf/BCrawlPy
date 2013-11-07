from bcrawl.data import DB

class Repository(object):

	def __init__(self, session):
		self.session = session

	def add_query(self, provider, text, start_day):
		query = DB.Query(provider, text, start_day)
		self.session.add(query)
		self.session.commit()
		return query

	def get_queries(self, provider_):
		return self.session.query(DB.Query).filter_by(provider=provider_).all()

	def add_day_for_query(self, query_id_, day_):
		day_query = DB.DayQuery(query_id = query_id_, day = day_, status = DB.DayQuery.STATUS_NEW)
		self.session.add(day_query)
		self.session.commit()
		return day_query

	def get_day_queries(self, query_id_):
		return self.session.query(DB.DayQuery).filter_by(query_id=query_id_).order_by("day").all()

	def get_day_queries_with_status(self, query_id_, status_):
		return self.session.query(DB.DayQuery).filter_by(query_id=query_id_, status=status_).order_by("day").all()
		
		