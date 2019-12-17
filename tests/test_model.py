import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project_app import app,db
from main.models import *
from datetime import datetime

import unittest

#Setting the testing enviorment for Testing the model
class ModelTest(unittest.TestCase):

#Add user model
    def test_add_user(self):
        user = users("admin","admin_username","admin@mun.ca","default")
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.name, "admin")
        self.assertEqual(user.username, "admin_username")
        self.assertEqual(user.email, "admin@mun.ca")
        self.assertEqual(user.password, "default")
        assert user in db.session
        db.session.delete(user)
        db.session.commit()

#Testing the Posts Model
    def test_add_topic(self):
        date=datetime.utcnow()
        topics = Topics("title by admin","admin","booody byyy adminmmm ",date)
        db.session.add(topics)
        db.session.commit()
        self.assertEqual(topics.title, "title by admin")
        self.assertEqual(topics.author, "admin")
        self.assertEqual(topics.body, "booody byyy adminmmm ")
        assert topics in db.session
        db.session.delete(topics)
        db.session.commit()

#Testing the Comments Model
    def test_add_comment(self):
        comment = Comments("comment by admin",0,"comment body by adminmmm ")
        db.session.add(comment)
        db.session.commit()
        assert comment in db.session
        self.assertEqual(comment.comment_writer, "comment by admin")
        self.assertEqual(comment.body_comment, "comment body by adminmmm ")

        db.session.delete(comment)
        db.session.commit()

if __name__ == '__main__':
    unittest.main()
