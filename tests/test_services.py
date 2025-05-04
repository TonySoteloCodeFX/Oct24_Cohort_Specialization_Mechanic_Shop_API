from app import create_app
from app.models import db
import unittest

class TestService(unittest.TestCase):
    def setUp(self):    #------------------------------------------------------ Service Setup
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def test_create_service(self): #------------------------------------------------------ Create Service Test Passed 🙂
        service_payload = {
            "service_desc": "Brake Inspection"
        }

        response = self.client.post('/services/', json=service_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['service_desc'], "Brake Inspection")

    def test_invalid_creation(self): #------------------------------------------------------ Invalid Create Service Test Passed 🙂
        service_payload = {}  # Missing required field

        response = self.client.post('/services/', json=service_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['service_desc'], ['Missing data for required field.'])
    
    def test_get_services(self): #------------------------------------------------------ Get All Services Test Passed 🙂
        self.client.post('/services/', json={"service_desc": "Tire Rotation"})
        self.client.post('/services/', json={"service_desc": "Battery Check"})

        response = self.client.get('/services/')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        descs = [service["service_desc"] for service in data]

        self.assertIn("Tire Rotation", descs)
        self.assertIn("Battery Check", descs)
    
    def test_get_service_by_id(self): #------------------------------------------------------ Get Service By ID Test Passed 🙂
        post_response = self.client.post('/services/', json={"service_desc": "Alignment"})

        service_id = post_response.get_json()['id']
        get_response = self.client.get(f'/services/{service_id}')

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json['service_desc'], "Alignment")

