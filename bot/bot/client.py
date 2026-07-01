import requests
import hashlib
import hmac
import time
from urllib.parse import urlencode
import logging

logger = logging.getLogger("trading_bot")

class BinanceFuturesClient:
    BASE_URL = "https://testnet.binancefuture.com"
    
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/json"
        })
    
    def _generate_signature(self, params: dict) -> str:
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _request(self, method: str, endpoint: str, params: dict = None, signed: bool = False):
        url = self.BASE_URL + endpoint
        if params is None:
            params = {}
        
        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["recvWindow"] = 5000
            signature = self._generate_signature(params)
            params["signature"] = signature
        
        logger.debug(f"Request: {method} {url} params={params}")
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params)
            elif method.upper() == "POST":
                response = self.session.post(url, params=params)  # POST params as query string
            else:
                raise ValueError("Unsupported HTTP method")
            
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Response: {data}")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Network/HTTP error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
    
    def get_account_info(self):
        """Fetch account info (for validation)."""
        return self._request("GET", "/fapi/v2/account", signed=True)
    
    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
        """
        Place an order on Binance Futures.
        Supports MARKET, LIMIT, STOP_LIMIT.
        """
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": float(quantity)
        }
        
        if order_type.upper() in ("LIMIT", "STOP_LIMIT"):
            if price is None:
                raise ValueError("Price is required for LIMIT and STOP_LIMIT orders")
            params["price"] = str(price)
            params["timeInForce"] = "GTC"  # Good till cancelled
        
        if order_type.upper() == "STOP_LIMIT":
            if stop_price is None:
                raise ValueError("stopPrice is required for STOP_LIMIT")
            params["stopPrice"] = str(stop_price)
        
        logger.info(f"Placing order: {params}")
        result = self._request("POST", "/fapi/v1/order", params=params, signed=True)
        logger.info(f"Order placed: {result}")
        return result
