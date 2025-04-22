# okx_trade.py
import requests
import time
import hmac
import hashlib
import base64
import os
import json

API_KEY = os.getenv("OKX_API_KEY")
SECRET_KEY = os.getenv("OKX_SECRET_KEY")
PASSPHRASE = os.getenv("OKX_PASSPHRASE")

if not all([API_KEY, SECRET_KEY, PASSPHRASE]):
    raise ValueError("Missing API credentials. Check environment variables.")

def place_market_order(symbol, side, size):
    url = "https://www.okx.com/api/v5/trade/order"
    timestamp = str(time.time())
    body = {
        "instId": symbol,
        "tdMode": "cash",
        "side": side,
        "ordType": "market",
        "sz": str(size)
    }
    message = timestamp + 'POST' + '/api/v5/trade/order' + json.dumps(body, separators=(',', ':'))
    signature = base64.b64encode(hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).digest()).decode()

    headers = {
        "OK-ACCESS-KEY": API_KEY,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=body, headers=headers)
    return response.json()
