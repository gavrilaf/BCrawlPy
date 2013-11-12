
# Mock queue for test purposes

class MockQueue(object):
	def __init__(self):
		self.items = []

	def put(self, p):
		self.items.append(p)