from flask import Flask
import unittest
import main 
import pytest

class FlaskTestCase(unittest.TestCase):

    def test_index(self):
        tester = main.app.test_client()
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        tester = main.app.test_client()
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_free(self):
        tester = main.app.test_client()
        response = tester.get('/free_hours', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        tester = main.app.test_client()
        response = tester.get('/signup', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_course(self):
        tester = main.app.test_client()
        response = tester.get('/course', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_assignment(self):
        tester = main.app.test_client()
        response = tester.get('/assignment', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_workspace(self):
        tester = main.app.test_client()
        response = tester.get('/workspace', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
if __name__ == '__main__':
    unittest.main()