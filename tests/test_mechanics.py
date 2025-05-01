from app import create_app
from app.models import db, Mechanic
from app.utils.auth import encode_token
import unittest


class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.mechanic = Mechanic(
            name='test_user',
            email='test@email.com',
            phone='test_phone',
            address='test_address',
            title='test_title',
            salary=50000.00,
            password='test_password' 
            )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.token = encode_token(1,'staff')
        self.client = self.app.test_client()

    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "661-202-9461",
            "address": "Los Angeles, CA",
            "title": "Staff",
            "salary": "60000",
            "password": "123"
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")

    def test_invalid_creation(self):
        mechanic_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "address": "Los Angeles, CA",
            "title": "Staff",
            "salary": "60000",
            "password": "123"
        }

        response = self.client.post('/mechanics/',json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['phone'],['Missing data for required field.'])

    def test_login_mechanic(self):
        credentials = {
            "email": "test@email.com",
            "password": "test_password"
        }

        response = self.client.post('/mechanics/login',json=credentials)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']