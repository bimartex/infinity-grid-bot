import time, hmac, hashlib, requests
import json

class BitgetAPI:
    def __init__(self, config):
        self.api_key = config['api_key']
        self.secret = config['api_secret']
        self.passphrase = config['passphrase']
        self.base_url = 'https://api.bitget.com'

    def _headers(self, method, endpoint, body=''):
        timestamp = str(int(time.time() * 1000))
        message = timestamp + method + endpoint + body
        sign = hmac.new(self.secret.encode(), message.encode(), hashlib.sha256).hexdigest()
        return {
            'ACCESS-KEY': self.api_key,
            'ACCESS-SIGN': sign,
            'ACCESS-TIMESTAMP': timestamp,
            'ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }

    def get_price(self, symbol):
        url = f'/api/spot/v1/market/ticker?symbol={symbol}'
        resp = requests.get(self.base_url + url)
        return float(resp.json()['data']['last'])

    def place_order(self, symbol, price, size, side):
        endpoint = '/api/spot/v1/trade/orders'
        url = self.base_url + endpoint
        body = json.dumps({
            "symbol": symbol,
            "price": str(price),
            "size": str(size),
            "side": side,
            "orderType": "limit"
        })
        headers = self._headers("POST", endpoint, body)
        return requests.post(url, headers=headers, data=body).json()
