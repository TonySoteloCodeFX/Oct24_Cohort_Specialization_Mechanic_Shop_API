from app import create_app
from app.models import db
import unittest

class TestCustomer(unittest.TestCase):
    def setUp(self):    #------------------------------------------------------ Customer Setup
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def test_create_customer(self): #------------------------------------------------------ Create Customer Test Passed 🙂
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "661-202-9461"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")

    def test_invalid_creation(self):    #------------------------------------------------------ Invalid Create Customer Test Passed 🙂
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com"
        }

        response = self.client.post('/customers/',json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['phone'],['Missing data for required field.'])

    def test_get_customers(self):   #------------------------------------------------------ Get Customers Test Passed 🙂
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "661-202-9461"
        }

        response_post = self.client.post('/customers/', json=customer_payload)  
        self.assertEqual(response_post.status_code, 201)

        response_get = self.client.get('/customers/')   
        self.assertEqual(response_get.status_code, 200)

        data = response_get.get_json()  

        customer_exists = False

        for customer in data:   
            if customer['name'] == "John Doe":
                customer_exists = True
                break 
        self.assertTrue

    def test_get_customer_by_id(self):  #------------------------------------------------------ Get Customers By ID Test Passed 🙂
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "661-202-9461"
        }

        post_response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(post_response.status_code, 201)

        customer_id = post_response.get_json()['id']

        get_response = self.client.get(f'/customers/{customer_id}')
        self.assertEqual(get_response.status_code, 200)

        customer_data = get_response.get_json()
        self.assertEqual(customer_data['name'], "John Doe")

    def test_update_customer(self): #------------------------------------------------------ Update Customer Test Passed 🙂
        original_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "661-202-9461"
        }

        post_response = self.client.post('/customers/', json=original_payload)
        self.assertEqual(post_response.status_code, 201)

        customer_id = post_response.get_json()['id']

        updated_payload = {
            "name": "Johnny Dough",
            "email": "johnny@email.com",
            "phone": "123-456-7890"
        }

        put_response = self.client.put(f'/customers/{customer_id}', json=updated_payload)
        self.assertEqual(put_response.status_code, 200)

        updated_data = put_response.get_json()
        self.assertEqual(updated_data['name'], "Johnny Dough")
        self.assertEqual(updated_data['email'], "johnny@email.com")
        self.assertEqual(updated_data['phone'], "123-456-7890")

    def test_delete_customer(self):  #------------------------------------------------------ Delete Customer Test Passed 🙂
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "661-202-9461"
        }

        post_response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(post_response.status_code, 201)

        customer_id = post_response.get_json()['id']

        delete_response = self.client.delete(f'/customers/{customer_id}')
        self.assertEqual(delete_response.status_code, 200)
