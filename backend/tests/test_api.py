import unittest
from app import app  # מייבאים את אובייקט ה-Flask מהקובץ app.py

class TestCurrencyAPI(unittest.TestCase):
    def setUp(self):
        # before each test – יוצרים client חדש
        self.client = app.test_client()

    # ---------- /health ----------

    def test_health_ok(self):
        """בודק שה-GET /health מחזיר 200 ו-json נכון"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data, {"status": "ok"})

    # ---------- /convert – מקרה תקין ----------

    def test_convert_valid_request(self):
        """בדיקה למקרה תקין: המרה מ-USD ל-EUR"""
        payload = {
            "amount": 100,
            "from": "USD",
            "to": "EUR"
        }

        response = self.client.post("/convert", json=payload)
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        # בודקים שהשדות קיימים
        self.assertIn("amount", data)
        self.assertIn("from", data)
        self.assertIn("to", data)
        self.assertIn("result", data)
        self.assertIn("rate", data)

        # בודקים ערכים בסיסיים
        self.assertEqual(data["amount"], 100)
        self.assertEqual(data["from"], "USD")
        self.assertEqual(data["to"], "EUR")

        # לא נבדוק ערך מדויק לגמרי (צפים) – רק שהוא גדול מ-0
        self.assertGreater(data["result"], 0)

    # ---------- /convert – חסרים שדות ----------

    def test_convert_missing_fields(self):
        """בדיקה כשחסרים שדות – צריך לקבל סטטוס 400"""
        payload = {
            "amount": 100,
            # חסר "from"
            "to": "EUR"
        }

        response = self.client.post("/convert", json=payload)
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn("error", data)
        self.assertIn("required", data["error"])

    # ---------- /convert – amount לא מספר ----------

    def test_convert_amount_not_number(self):
        """בדיקה כש-amount הוא מחרוזת לא מספרית"""
        payload = {
            "amount": "abc",
            "from": "USD",
            "to": "EUR"
        }

        response = self.client.post("/convert", json=payload)
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn("error", data)
        self.assertIn("amount must be a number", data["error"])

    # ---------- /convert – מטבע מקור לא נתמך ----------

    def test_convert_unsupported_from_currency(self):
        """בדיקה למטבע מקור לא נתמך"""
        payload = {
            "amount": 100,
            "from": "ILS",  # לא קיים ב-RATES_TO_USD
            "to": "USD"
        }

        response = self.client.post("/convert", json=payload)
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn("error", data)
        self.assertIn("Unsupported 'from' currency", data["error"])

    # ---------- /convert – מטבע יעד לא נתמך ----------

    def test_convert_unsupported_to_currency(self):
        """בדיקה למטבע יעד לא נתמך"""
        payload = {
            "amount": 100,
            "from": "USD",
            "to": "ILS"  # לא קיים ב-RATES_TO_USD
        }

        response = self.client.post("/convert", json=payload)
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn("error", data)
        self.assertIn("Unsupported 'to' currency", data["error"])


if __name__ == "__main__":
    unittest.main()



# python3 -m venv venv
# source venv/bin/activate

# pip install -r requirements.txt
# python -m unittest


#run by pytest
#pip install pytest
#pytest