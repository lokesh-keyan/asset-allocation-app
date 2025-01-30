import unittest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
from myapp import myapp

class TestAssetAllocation(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(myapp)
    
    def test_calculate_allocation(self):
        response = self.client.post("/calculate", json={
            "total": 100.0,
            "holdings": [
                {"name": "stock", "amount": 80.0},
                {"name": "bond", "amount": 20.0}
            ]
        })

        self.assertEqual(response.status_code, 200)
        data = response.json()["allocations"]
        excepted = [
                {"name": "stock", "percentage": 80.0},
                {"name": "bond", "percentage": 20.0}
        ]
        self.assertEqual(data, excepted)

    def test_negative_values(self):
        response = self.client.post("/calculate", json={
            "total": 1000,
            "holdings": [
                {"name": "Stock A", "amount": -500}
            ]
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()["allocations"]
        self.assertEqual(data[0]["percentage"], -50.0)  # Handling negative amounts correctly

if __name__ == "__main__":
    unittest.main()