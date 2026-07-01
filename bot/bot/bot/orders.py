from .client import BinanceFuturesClient
from .validators import *
import logging

logger = logging.getLogger("trading_bot")

def place_order(client: BinanceFuturesClient, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
    """
    High-level order placement with validations.
    """
    # Validations
    if not validate_symbol(symbol):
        raise ValueError(f"Invalid symbol: {symbol}")
    if not validate_side(side):
        raise ValueError(f"Invalid side: {side}. Use BUY or SELL.")
    if not validate_order_type(order_type):
        raise ValueError(f"Invalid order_type: {order_type}. Use MARKET, LIMIT, or STOP_LIMIT.")
    if not validate_quantity(quantity):
        raise ValueError(f"Quantity must be > 0: {quantity}")
    
    if order_type.upper() in ("LIMIT", "STOP_LIMIT"):
        if not validate_price(price, order_type):
            raise ValueError(f"Invalid price for {order_type}: {price}")
    
    if order_type.upper() == "STOP_LIMIT" and stop_price is None:
        raise ValueError("stop_price is required for STOP_LIMIT")
    
    # Place order via client
    return client.place_order(symbol, side, order_type, quantity, price, stop_price)
