from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Conectar na Binance Testnet
client = Client(API_KEY, API_SECRET, testnet=True)

def get_recent_candles(symbol="BTCUSDT", interval="1m", limit=100):
    candles = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    return candles

if __name__ == "__main__":
    data = get_recent_candles()
    print(f"Últimos {len(data)} candles para BTCUSDT:")
    for candle in data:
        print(candle)
