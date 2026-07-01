import re

def validate_symbol(symbol: str) -> bool:
    """Basic check: only letters and digits, e.g., BTCUSDT."""
    return bool(re.match(r"^[A-Z0-9]+$", symbol))

def validate_side(side: str) -> bool:
    return side.upper() in ("BUY", "SELL")

def validate_order_type(order_type: str) -> bool:
    return order_type.upper() in ("MARKET", "LIMIT", "STOP_LIMIT")

def validate_quantity(quantity: float) -> bool:
    return quantity > 0

def validate_price(price: float, order_type: str) -> bool:
    if order_type.upper() in ("LIMIT", "STOP_LIMIT"):
        return price > 0
    return True  # MARKET orders don't need price
