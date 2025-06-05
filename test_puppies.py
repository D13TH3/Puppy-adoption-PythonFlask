import unittest
from myproject import app, db
from myproject.models import Puppy

class PuppiesTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_puppy(self):
        response = self.app.post('/puppies/add', data={'name': 'TestPup'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TestPup', response.data)

    def test_list_puppies(self):
        with app.app_context():
            pup = Puppy(name='ListPup')
            db.session.add(pup)
            db.session.commit()
        response = self.app.get('/puppies/list')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ListPup', response.data)

    def test_delete_puppy(self):
        with app.app_context():
            pup = Puppy(name='DeleteMe')
            db.session.add(pup)
            db.session.commit()
            pup_id = pup.id

        response = self.app.post('/puppies/delete', data={'id': pup_id}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'DeleteMe', response.data)

if __name__ == '__main__':
    unittest.main()
