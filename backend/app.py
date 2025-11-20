
import os
from flask import Flask, jsonify, request

# נשים את תקיית הבילד של ה-React בתור static_folder
app = Flask(__name__, static_folder="frontend-dist", static_url_path="/")

from flask_cors import CORS
CORS(app)

RATES_TO_USD = {
    "USD": 1.0,
    "EUR": 1.1,
    "GBP": 1.3,
    "JPY": 0.009,
}

SUPPORTED_CURRENCIES = set(RATES_TO_USD.keys())


def convert_amount(amount: float, from_currency: str, to_currency: str) -> float:
    amount_in_usd = amount * RATES_TO_USD[from_currency]
    converted = amount_in_usd / RATES_TO_USD[to_currency]
    return converted


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.post("/convert")
def convert():
    data = request.get_json(silent=True) or {}

    amount = data.get("amount")
    from_currency = data.get("from")
    to_currency = data.get("to")

    if amount is None or from_currency is None or to_currency is None:
        return jsonify({"error": "amount, from, and to are required"}), 400

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "amount must be a number"}), 400

    from_currency = str(from_currency).upper()
    to_currency = str(to_currency).upper()

    if from_currency not in SUPPORTED_CURRENCIES:
        return jsonify({"error": f"Unsupported 'from' currency: {from_currency}"}), 400
    if to_currency not in SUPPORTED_CURRENCIES:
        return jsonify({"error": f"Unsupported 'to' currency: {to_currency}"}), 400

    result = convert_amount(amount, from_currency, to_currency)
    rate = result / amount if amount != 0 else None

    return jsonify({
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
        "result": round(result, 4),
        "rate": round(rate, 6) if rate is not None else None
    }), 200


# ===== מסלול שמגיש את ה-React build =====
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    """
    כל בקשה ל-"/" או לכל path אחר תנסה להחזיר קובץ סטטי מה-build,
    ואם אין – תחזיר index.html (SPA routing).
    """
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return app.send_static_file(path)
    return app.send_static_file("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # ברירת מחדל: 8080
    app.run(host="0.0.0.0", port=port)







# from flask import Flask, jsonify, request
# from flask_cors import CORS

# app = Flask(__name__)
# # מאפשרים בקשות מ־React שרץ על פורט אחר (למשל 5173)
# CORS(app)

# # שערי המרה – יחס ל־USD (1 יחידה מהמטבע = כמה USD)
# RATES_TO_USD = {
#     "USD": 1.0,
#     "EUR": 1.1,   # 1 EUR ≈ 1.1 USD (דוגמה קשיחה)
#     "GBP": 1.3,   # 1 GBP ≈ 1.3 USD
#     "JPY": 0.009  # 1 JPY ≈ 0.009 USD
# }

# SUPPORTED_CURRENCIES = set(RATES_TO_USD.keys())


# def convert_amount(amount: float, from_currency: str, to_currency: str) -> float:
#     """
#     ממיר סכום מ־from_currency ל־to_currency בעזרת המטבע הבסיסי USD.
#     """
#     # ממירים קודם ל־USD
#     amount_in_usd = amount * RATES_TO_USD[from_currency]
#     # ואז מ־USD למטבע היעד
#     converted = amount_in_usd / RATES_TO_USD[to_currency]
#     return converted


# @app.get("/health")
# def health():
#     """בדיקת בריאות – אפשר להשתמש ל־readiness / liveness."""
#     return jsonify({"status": "ok"}), 200


# @app.post("/convert")
# def convert():
#     """
#     מקבל JSON:
#     {
#       "amount": 100,
#       "from": "USD",
#       "to": "EUR"
#     }
#     ומחזיר:
#     {
#       "amount": 100,
#       "from": "USD",
#       "to": "EUR",
#       "result": 95.5,
#       "rate": 0.955
#     }
#     """
#     data = request.get_json(silent=True) or {}

#     amount = data.get("amount")
#     from_currency = data.get("from")
#     to_currency = data.get("to")

#     # ולידציה בסיסית
#     if amount is None or from_currency is None or to_currency is None:
#         return jsonify({"error": "amount, from, and to are required"}), 400

#     try:
#         amount = float(amount)
#     except ValueError:
#         return jsonify({"error": "amount must be a number"}), 400

#     from_currency = str(from_currency).upper()
#     to_currency = str(to_currency).upper()

#     if from_currency not in SUPPORTED_CURRENCIES:
#         return jsonify({"error": f"Unsupported 'from' currency: {from_currency}"}), 400
#     if to_currency not in SUPPORTED_CURRENCIES:
#         return jsonify({"error": f"Unsupported 'to' currency: {to_currency}"}), 400

#     result = convert_amount(amount, from_currency, to_currency)

#     # אפשר גם לחשב את השער הישיר (כמה מטבע יעד על 1 מהמקור)
#     rate = result / amount if amount != 0 else None

#     return jsonify({
#         "amount": amount,
#         "from": from_currency,
#         "to": to_currency,
#         "result": round(result, 4),
#         "rate": round(rate, 6) if rate is not None else None
#     }), 200


# if __name__ == "__main__":
#     # Flask יקשיב כברירת מחדל על 5000
#     app.run(host="0.0.0.0", port=5000, debug=True)






# cd backend
# python -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# python app.py


# //בדיקה מהירה
# curl http://localhost:5000/health
# curl -X POST http://localhost:5000/convert \
#   -H "Content-Type: application/json" \
#   -d '{"amount": 100, "from": "USD", "to": "EUR"}'
