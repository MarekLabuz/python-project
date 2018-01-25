import unittest
from server import app
import util
 
class FlaskrTestCase(unittest.TestCase):

    def test_return_status_200_query(self):
        tester = app.test_client(self)
        response = tester.get('/movies?query=bieber', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_return_status_200_movie(self):
        tester = app.test_client(self)
        response = tester.get('/movie?id=83824&actor_id=', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_response_contains_title(self):
        tester = app.test_client(self)
        response = tester.get('/movie?id=83824&actor_id=', content_type='html/text')
        self.assertIn('\"title\":', response.get_data(as_text=True))

    def test_response_contatins_people(self):
        tester = app.test_client(self)
        response = tester.get('/movie?id=83824&actor_id=', content_type='html/text')
        self.assertIn('\"people\":', response.get_data(as_text=True))

    def test_response_contains_id_of_asked_actor(self):
        tester = app.test_client(self)
        response = tester.get('/movie?id=83824&actor_id=108215', content_type='html/text')
        self.assertIn('\"id\": \"108215', response.get_data(as_text=True) )

    def test_saved_actor_in_database(self):
        tester = app.test_client(self)
        response = tester.get('/movie?id=83824&actor_id=108215', content_type='html/text')
        self.assertFalse(util.person_not_exist('26209'))


if __name__ == '__main__':
	unittest.main()