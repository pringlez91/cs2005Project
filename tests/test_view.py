import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
basedir = os.path.abspath(os.path.dirname(__file__))

import unittest

from project_app import app,db


#Testing the UserTest for the main app
class UserTest(unittest.TestCase):

#Setting up the test database
    def setUp(self):
        self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        self.app = app.test_client()
        db.create_all()
#Tearing down the test database
    def tearDown(self):
        db.session.remove()
        db.drop_all()


    ##Helper Methods
    def signup(self,name,username,email,password,confirm):
        return self.app.post('/signup', data=dict(
            name=name,
            username=username,
            email=email,
            password=password,
            confirm=confirm,
            ),
            follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)


    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def add_post(self, title, body):
        return self.app.post('/add_post', data=dict(
            title=title,
            body=body
        ), follow_redirects=True)


    ##Tests
    def test_main_page(self):
        rv = self.app.get('/', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        chec=[b'Surviving',b'Sign Up',b'Login',b'Home',b'Topics']
        for items in chec:
            assert items in rv.data

    def test_about_page(self):
        rv = self.app.get('/about', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        assert b'About Us' in rv.data

    def test_topics_page(self):
        rv = self.app.get('/topics', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        assert b'Topics' in rv.data

    def test_dashboard(self):
        rv = self.app.get('/dashboard', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        assert b'Add Post' not in rv.data
        assert b'Create Group' not in rv.data
        rv = self.signup('admin','admin_u','admin@mun.ca','default','default')
        rv = self.login('admin_u', 'default')
        assert b'Add Post' in rv.data
        assert b'Create Group' in rv.data


    def test_signup(self):
        rv = self.signup('admin','admin_u','admin@mun.ca','default','default')
        self.assertEqual(rv.status_code, 200)
        rv = self.signup('admin','admin_u','admin@mun.ca','default','default1')
        assert b'Passwords do not match' in rv.data

    def test_login(self):
        rv = self.signup('admin','admin_u','admin@mun.ca','default','default')
        rv = self.login('admin_u', 'default')
        assert b'You are now logged in' in rv.data
        assert b'Login' not in rv.data
        assert b'Username' not in rv.data
        assert b'Password' not in rv.data
        rv = self.login('adminx', 'default')
        assert b'Username and password doesnt match' in rv.data
        rv = self.login('admin', 'defaultx')
        assert b'Username and password doesnt match' in rv.data

    def test_logout(self):
        rv = self.signup('admin','admin_u','admin@mun.ca','default','default')
        rv = self.login('admin_u', 'default')
        rv = self.logout()
        assert b'You are now logged out' in rv.data
        assert b'Login' in rv.data
        assert b'Username' in rv.data
        assert b'Password' in rv.data


    def test_add_post(self):
        rv = self.signup('admin','admin_u','admin@mun.ca','default','default')
        rv = self.login('admin_u', 'default')
        rv = self.add_post('admin title','body too short')
        self.assertEqual(rv.status_code, 200)
        assert b'Field must be at least 30 characters long.' in rv.data
        rv = self.add_post('admin title','body created by the adminstrator to test')
        self.assertEqual(rv.status_code, 200)
        assert b'Post Created' in rv.data


if __name__ == '__main__':
    unittest.main()
