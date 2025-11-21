import requests
import time
import unittest
import pytest
BASE_URL = "http://localhost:8080"

@pytest.mark.integration
class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # מחכים כמה שניות שהקונטיינר יעלה
        max_wait = 10
        for _ in range(max_wait):
            try:
                r = requests.get(f"{BASE_URL}/health")
                if r.status_code == 200:
                    return
            except Exception:
                pass
            time.sleep(1)

        raise RuntimeError("Container did not become ready")

    def test_health(self):
        r = requests.get(f"{BASE_URL}/health")
        self.assertEqual(r.status_code, 200)

    def test_convert(self):
        payload = {"amount": 100, "from": "USD", "to": "EUR"}
        r = requests.post(f"{BASE_URL}/convert", json=payload)

        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn("result", data)
        self.assertGreater(data["result"], 0)