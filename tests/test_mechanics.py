from app import create_app
from app.models import db, Mechanic
from app.utils.auth import encode_token
from werkzeug.security import generate_password_hash
import unittest


class TestMechanic(unittest.TestCase):
    def setUp(self):    #------------------------------------------------------ Mechanic Setup
        self.app = create_app("TestingConfig")
        self.mechanic = Mechanic(
            name='test_user',
            email='test@email.com',
            phone='test_phone',
            address='test_address',
            title='test_title',
            salary=50000,
            password=generate_password_hash('test_password') 
            )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()

    def test_create_mechanic(self): #------------------------------------------------------ Create Mechanic Test Passed 🙂
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

    def test_invalid_creation(self):    #------------------------------------------------------ Invalid Create Customer Test Passed 🙂
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

    def test_login_mechanic(self):  #------------------------------------------------------ Mechanic Login Test Passed 🙂
        credentials = {
            "email": "test@email.com",
            "password": "test_password"
        }

        response = self.client.post('/mechanics/login',json=credentials)
        self.assertEqual(response.status_code,200)
        return response.json['Token']
    
    def test_get_all_mechanics(self):   #------------------------------------------------------ Get All Mechanics Test Passed 🙂
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()  

        mechanic_exists = False

        for mechanic in data:   
            if mechanic['email'] == "test@email.com":
                mechanic_exists = True
                break 
        self.assertTrue

    def test_get_mechanic_by_id(self):  #------------------------------------------------------ Get Mechanics By ID Test Passed 🙂
        response = self.client.get('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'test_user')

    def test_get_mechanic_invalid_id(self): #------------------------------------------------------ Invalid Mechanics ID Test Passed 🙂
        response = self.client.get('/mechanics/5')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Mechanic does not exist.')

    def test_update_mechanic(self): #------------------------------------------------------ Update Mechanic Test Passed 🙂
        updated_data = {
            "name": "Updated Name",
            "email": "test@email.com",
            "phone": "updated_phone",
            "address": "updated_address",
            "title": "Lead Mechanic",
            "salary": 55000,
            "password": "new_password"
        }
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self.client.put('/mechanics/', json=updated_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], 'Lead Mechanic')






