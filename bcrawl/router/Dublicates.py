from bcrawl.base import MQData
import PostInfoDB

class Handler(object):
	def __init__(self, db):
		self.db = db

	def process(self, post):
		"""
			Check post.link in dublicates db
		"""
		pinfo = self.db.find_pinfo(post.link)
		print pinfo
		
		if pinfo is None: # New post
			pinfo = self.pinfo_from_post(post)
			self.store_pinfo(pinfo)
		else:
			print 1
			post.status = MQData.Post.DUBLICATE

			if post.query_id not in pinfo.queries:
				print 2
				post.status = MQData.Post.NEW_LINK
				pinfo.queries.append(post.query_id)

			if pinfo.publish_date < post.publish_date:
				print 3
				post.status = MQData.Post.UPDATED
				pinfo.publish_date = post.publish_date

		print 'Before storing: %s' % str(pinfo)
		self.store_pinfo(pinfo)

		return post

	def pinfo_from_post(self, post):
		pinfo = PostInfoDB.PostInfo()

		pinfo.link = post.link
		pinfo.publish_date = post.publish_date
		pinfo.queries.append(post.query_id)

		return pinfo

	def store_pinfo(self, pinfo):
		self.db.store_pinfo(pinfo)