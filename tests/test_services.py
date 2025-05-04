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
    
    def test_update_service(self): #------------------------------------------------------ Update Service Test Passed 🙂
        post_response = self.client.post('/services/', json={"service_desc": "Oil Flush"})
        service_id = post_response.get_json()['id']

        updated_payload = {
            "service_desc": "Transmission Flush"
        }

        put_response = self.client.put(f'/services/{service_id}', json=updated_payload)
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(put_response.json['service_desc'], "Transmission Flush")
    
    def test_delete_service(self): #------------------------------------------------------ Delete Service Test Passed 🙂
        post_response = self.client.post('/services/', json={"service_desc": "Coolant Replacement"})
        service_id = post_response.get_json()['id']

        delete_response = self.client.delete(f'/services/{service_id}')
        self.assertEqual(delete_response.status_code, 200)

        get_after_delete = self.client.get(f'/services/{service_id}')
        self.assertEqual(get_after_delete.status_code, 200)
        self.assertEqual(get_after_delete.json.get("error"), "Service does not exist.")

