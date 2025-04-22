# app.py
from flask import Flask, request, jsonify
from okx_trade import place_market_order

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    symbol = data.get("symbol")
    side = data.get("side")
    amount = data.get("amount")

    if not symbol or not side or not amount:
        return jsonify({"error": "Missing required fields"}), 400

    result = place_market_order(symbol, side, amount)
    return jsonify(result)
