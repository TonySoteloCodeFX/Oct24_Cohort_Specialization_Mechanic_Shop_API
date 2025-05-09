from app import create_app
from app.models import db, Customer, Mechanic, Service, ItemDesc, SerialItem
from datetime import date
import unittest


class TestTicket(unittest.TestCase):
    def setUp(self):  # ------------------------------------------------------ Ticket Setup
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            
            self.customer = Customer(
                name="Jane Doe", email="jane@example.com", phone="123-456-7890"
            )
            self.mechanic = Mechanic(
                name="Mike Wrench", email="mike@example.com", phone="321-654-0987",
                address="123 Auto Lane", title="Lead Tech", salary=75000.0,
                password="secure123"
            )
            self.service = Service(service_desc="Engine Diagnostics")
            self.item_desc = ItemDesc(name="Air Filter", price=25.0)
            self.serial_item = SerialItem(description=self.item_desc)

            db.session.add_all([
                self.customer, self.mechanic, self.service,
                self.item_desc, self.serial_item
            ])
            db.session.commit()

            
            self.customer_id = self.customer.id
            self.mechanic_id = self.mechanic.id
            self.service_id = self.service.id
            self.description_id = self.item_desc.id

        self.client = self.app.test_client()
    
    def create_ticket(self): # ------------------------------------------------------ Create Ticket Passed 🙂
        payload = {
            "service_date": "2025-05-04",
            "vin": "1HGCM82633A004352",
            "customer_id": self.customer_id,
            "mechanic_ids": [self.mechanic_id],
            "service_ids": [self.service_id]
        }
        response = self.client.post('/tickets/', json=payload)
        self.assertEqual(response.status_code, 201)
        return response.get_json()  
    
    def test_create_ticket(self):  # ------------------------------------------------------ Create Ticket Passed 🙂
        payload = {
            "service_date": str(date.today()),
            "vin": "1HGCM82633A004352",
            "customer_id": self.customer_id,
            "mechanic_ids": [self.mechanic_id],
            "service_ids": [self.service_id]
        }

        response = self.client.post('/tickets/', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['vin'], payload['vin'])
    
    def test_get_all_tickets(self):  # ------------------------------------------------------ Get All Tickets 🙂
        self.test_create_ticket()
        response = self.client.get('/tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.get_json()), 1)
    
    def test_get_ticket_by_id(self):  # ------------------------------------------------------ Get Ticket by ID 🙂
        ticket = self.create_ticket()
        ticket_id = ticket['id']

        response = self.client.get(f'/tickets/{ticket_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], ticket_id)

    def test_update_ticket(self):  # ------------------------------------------------------ Update Ticket 🙂
        self.test_create_ticket()
        updated_payload = {
            "service_date": str(date.today()),
            "vin": "UPDATEDVIN123456",
            "customer_id": self.customer_id,
            "mechanic_ids": [self.mechanic_id],
            "service_ids": [self.service_id]
        }
        response = self.client.put('/tickets/1', json=updated_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['vin'], "UPDATEDVIN123456")
    
    def test_add_item_to_ticket(self):  # ------------------------------------------------------ Add Item to Ticket 🙂
        self.test_create_ticket()
        response = self.client.put(f"/tickets/1/add_item/{self.description_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Successfully added", response.json['message'])
    
    def test_add_item_out_of_stock(self):  # ------------------------------------------------------ Add Item Out of Stock 🙂
        self.test_create_ticket()
        self.client.put(f"/tickets/1/add_item/{self.description_id}")  
        response = self.client.put(f"/tickets/1/add_item/{self.description_id}") 
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "Item out of stock.")
    
