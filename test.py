import unittest
from server import app
 
class FlaskrTestCase(unittest.TestCase):

    # def test_1(self):
    #     tester = app.test_client(self)
    #     response = tester.get('/movies?query=bieber', content_type='html/text')
    #     self.assertEqual(response.status_code, 200)

    def test_2(self):
        tester = app.test_client(self)
        response = tester.get('/movie?id=83824&actor_id=', content_type='html/text')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
	unittest.main()