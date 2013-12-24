import unittest
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bcrawl.base import Consts, MQData
from bcrawl.db import DB, SearchDB, Posts


class PostsRepositoryTests(unittest.TestCase):

	def setUp(self):
		self.engine = create_engine('sqlite:///:memory:')
		DB.Base.metadata.create_all(self.engine)
		Session = sessionmaker(bind=self.engine)
		self.session = Session()

		self.rep = Posts.Repository(self.session)

	def tearDown(self):
		self.session.close()

	def test_BlogHost(self):
		self.assertEqual(len(self.rep.get_blog_hosts()), 0)

		name = 'vk.com'
		
		bh1 = self.rep.add_blog_host(name)
		self.assertIsNotNone(bh1)
		self.assertEqual(bh1.host, name)

		bh2 = self.rep.get_blog_host_by_id(bh1.id)
		self.assertIsNotNone(bh2)
		self.assertEqual(bh1.id, bh2.id)
		self.assertEqual(bh2.host, name)

		lst = self.rep.get_blog_hosts()
		self.assertEqual(len(lst), 1)
		self.assertEqual(bh1.id, lst[0].id)
		self.assertEqual(bh1.host, lst[0].host)

	def test_Author(self):
		self.assertEqual(len(self.rep.get_authors()), 0)

		name = 'autor-test'
		
		a1 = self.rep.add_author(name)
		self.assertIsNotNone(a1)
		self.assertEqual(a1.blog, name)

		a2 = self.rep.get_author_by_id(a1.id)
		self.assertIsNotNone(a2)
		self.assertEqual(a1.id, a2.id)
		self.assertEqual(a2.blog, name)

		lst = self.rep.get_authors()
		self.assertEqual(len(lst), 1)
		self.assertEqual(a1.id, lst[0].id)
		self.assertEqual(a1.blog, lst[0].blog)


	def test_AddPost(self):
		self.assertEqual(len(self.rep.get_posts_by_query(1)), 0)
		self.assertEqual(len(self.rep.get_authors()), 0)
		self.assertEqual(len(self.rep.get_blog_hosts()), 0)

		d2 = datetime.datetime.utcnow().replace(microsecond=0)
		d1 = d2 - datetime.timedelta(days=5)

		p = MQData.Post(query_id = 1, 
			provider = Consts.Providers.YANDEX,
			title = 'test title',
			link = 'test link',
			publish_date = d1,
			author = 'test author')

		p.host = 'test host'
		p.content = 'test content'
		collected = d2

		post = self.rep.add_post(p)
		self.assertIsNotNone(post)

		post = self.rep.get_post_by_id(post.id)

		self.assertEqual(post.title, 'test title')
		self.assertEqual(post.link, 'test link')
		self.assertEqual(post.publish_date.replace(microsecond=0), d1)
		self.assertEqual(post.collected_date.replace(microsecond=0), d2)

		author = self.rep.get_author_by_id(post.author_id)

		self.assertIsNotNone(author)
		self.assertEqual(author.blog, 'test author')


		host = self.rep.get_blog_host_by_id(post.blog_host_id)

		self.assertIsNotNone(host)
		self.assertEqual(host.host, 'test host')

		self.assertEqual(post.content.content, 'test content')

		content = self.rep.get_post_content_by_post_id(post.id)

		self.assertIsNotNone(content)
		self.assertEqual(content.content, post.content.content)



		