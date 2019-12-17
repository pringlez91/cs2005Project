
import unittest
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main.form import *

#This one is setting up the testing enviorment for the form
class TestForms(unittest.TestCase):
#Testing the login form
   def test_login_form(self):
       form=LoginForm(username='john',password='pass')
       form.validate()
       self.assertEqual(form.username.data,'john')
       self.assertEqual(form.password.data,'pass')
       self.assertNotEqual(form.username.data,'john1')
       self.assertNotEqual(form.password.data,'pass1')
#Testing the post form
   def test_topic_form(self):##test article form
       form=TopicForm(title='',body='tooshort')
       form.validate()
       self.assertEqual(form.title.errors,["Field must be between 1 and 200 characters long."])
       self.assertEqual(form.body.errors,["Field must be at least 30 characters long."])
       form=TopicForm(title='tooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooloooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog')
       form.validate()
       self.assertEqual(form.title.errors,["Field must be between 1 and 200 characters long."])
       form=TopicForm(title="test",body='testtttttttttttttttttttttttttttttttttttttttttttttttt')
       form.validate()
       self.assertEqual(form.title.data,"test")
       self.assertEqual(form.body.data,"testtttttttttttttttttttttttttttttttttttttttttttttttt")
#Testing the register form
   def test_register_form(self):##test registertion form

       form=SignUpForm(name='',username='joe',email='aaa',password='')
       form.validate()
       self.assertEqual(form.name.errors,["Field must be between 1 and 50 characters long."])
       self.assertEqual(form.username.errors,["Field must be between 4 and 25 characters long."])
       self.assertEqual(form.email.errors,["Field must be between 6 and 50 characters long."])
       self.assertEqual(form.password.errors,["This field is required."])
       form=SignUpForm(password='123',confirm='234')
       form.validate()
       self.assertEqual(form.password.errors,["Passwords do not match"])
       form=SignUpForm(name="test",username='test1',email='test@mun.ca',password='123456',confirm='12345')
       form.validate()
       self.assertEqual(form.name.data,"test")
       self.assertEqual(form.username.data,"test1")
       self.assertEqual(form.email.data,"test@mun.ca")
       self.assertEqual(form.password.data,"123456")
       self.assertEqual(form.confirm.data,"12345")
       self.assertEqual(form.password.errors,["Passwords do not match"])
#Testing the comment form
   def test_comment_form(self):
       form=CommentForm( body_comment='comment by admin')
       form.validate()
       self.assertEqual(form.body_comment.data,"comment by admin")

if __name__ == '__main__':
   unittest.main()
