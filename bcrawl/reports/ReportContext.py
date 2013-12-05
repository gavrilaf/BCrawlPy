from pymongo import MongoClient


class ReportContext(object):
	def __init__(self, report, mongo_db_path = 'bcrawl-reports'):
		self.mongo_client = MongoClient(tz_aware=True)
		self.mongo_db = self.mongo_client[mongo_db_path]

		self.report = report


	def get_report(self):
		return self.report.get_report(self.mongo_db)

	def close(self):
		self.mongo_client.close()