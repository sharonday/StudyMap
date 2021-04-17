from flask import Flask, request
import flask_testing
import unittest
import main 
import pytest

class FlaskTestCase(unittest.TestCase):

    def test_login_correct(self):
        with main.app.test_client() as tester:
            response = tester.post('/login-user/', 
            data=dict(username="test2", password="pass2", 
            follow_redirects=True)
            )
            user = main.get_current_user()
            self.assertEqual("test2", user)

    def test_create_correct(self):
        with main.app.test_client() as tester:
            response = tester.post('/create-user/', 
            data=dict(username="nicholas114", password="pass6",
            follow_redirects=True)
            )
            user = main.get_current_user()
            self.assertEqual("nicholas114", user)

    def test_create_course(self):
        with main.app.test_client() as tester:
            tester.post('/login-user/', 
            data=dict(username="test2", password="pass2", 
            follow_redirects=True)
            )
            response = tester.post('/add-course/', 
            data=dict(course1="ethics", course_colors="blue"))
            courses = main.get_courses()
            names = [x["name"] for x in courses]
            self.assertIn("ethics", names)

    def test_add_assignment(self):
       with main.app.test_client() as tester:
          tester.post('/login-user/', 
          data=dict(username="test2", password="pass2", 
          follow_redirects=True)
          )
          response = tester.post('/add-assignment/', 
          data=dict( hwname="essay3", hwdate="03/01/2022", hwcourse="ethics", hours="2"))
          assign = main.get_assignments()
          names = [u["name"] for u in assign]
          self.assertIn("essay3", names)

    def test_logout(self):
         with main.app.test_client() as tester:
            tester.post('/login-user/', 
            data=dict(username="test2", password="pass2", 
            follow_redirects=True)
            )
            user = main.get_current_user()
            main.logout()
            self.assertNotEqual(user, main.get_current_user())
            self.assertEqual(None, main.get_current_user())


if __name__ == '__main__':
    unittest.main()