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
