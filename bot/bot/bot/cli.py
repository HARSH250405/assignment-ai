#!/usr/bin/env python3
import argparse
import os
import sys
from dotenv import load_dotenv

from bot.client import BinanceFuturesClient
from bot.orders import place_order
from bot.logging_config import setup_logging

load_dotenv()  # Load from .env file if present

def main():
    # Setup logging
    logger = setup_logging("trading_bot.log")
    
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot CLI")
    parser.add_argument("--symbol", required=True, help="Trading pair symbol, e.g., BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT", "STOP_LIMIT"], help="Order type")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Price for LIMIT and STOP_LIMIT orders")
    parser.add_argument("--stop-price", type=float, help="Stop price for STOP_LIMIT orders")
    parser.add_argument("--api-key", help="Binance API key (can also set env BINANCE_API_KEY)")
    parser.add_argument("--api-secret", help="Binance API secret (can also set env BINANCE_API_SECRET)")
    
    args = parser.parse_args()
    
    # Get API credentials from args or environment
    api_key = args.api_key or os.getenv("BINANCE_API_KEY")
    api_secret = args.api_secret or os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        logger.error("API key and secret required. Set via --api-key/--api-secret or environment variables.")
        sys.exit(1)
    
    # Create client
    client = BinanceFuturesClient(api_key, api_secret)
    
    # Print summary
    logger.info("=== Order Request Summary ===")
    logger.info(f"Symbol: {args.symbol}")
    logger.info(f"Side: {args.side}")
    logger.info(f"Type: {args.type}")
    logger.info(f"Quantity: {args.quantity}")
    if args.price is not None:
        logger.info(f"Price: {args.price}")
    if args.stop_price is not None:
        logger.info(f"Stop Price: {args.stop_price}")
    
    try:
        result = place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price
        )
        # Print order response details
        logger.info("=== Order Response ===")
        logger.info(f"Order ID: {result.get('orderId')}")
        logger.info(f"Status: {result.get('status')}")
        logger.info(f"Executed Qty: {result.get('executedQty', '0')}")
        logger.info(f"Avg Price: {result.get('avgPrice', 'N/A')}")
        logger.info(f"Client Order ID: {result.get('clientOrderId')}")
        logger.info("Order placed successfully!")
    except Exception as e:
        logger.error(f"Order failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
