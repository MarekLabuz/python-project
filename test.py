import unittest
from server import app
import util
 
class FlaskrTestCase(unittest.TestCase):

    def test_1(self):
        tester = app.test_client(self)
        response = tester.get('/movies?query=bieber', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_2(self):
        tester = app.test_client(self)
        response = tester.get('/movie?id=83824&actor_id=', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_3(self):
        tester = app.test_client(self)
        response = tester.get('/movie?id=83824&actor_id=', content_type='html/text')
        self.assertIn('\"title\":', response.get_data(as_text=True))

    def test_4(self):
        tester = app.test_client(self)
        response = tester.get('/movie?id=83824&actor_id=', content_type='html/text')
        self.assertIn('\"people\":', response.get_data(as_text=True))


    def test_5(self):
        tester = app.test_client(self)
        response = tester.get('/movie?id=83824&actor_id=108215', content_type='html/text')
        self.assertIn('\"id\": \"108215', response.get_data(as_text=True) )

    def test_6(self):
        tester = app.test_client(self)
        response = tester.get('/movie?id=83824&actor_id=108215', content_type='html/text')
        self.assertFalse(util.person_not_exist('26209'))

# czy zawiera title <- struktura


if __name__ == '__main__':
	unittest.main()


	# powioazania wiele do wielu 