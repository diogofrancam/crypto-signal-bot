import os
from dotenv import load_dotenv
import requests
from binance_client import get_recent_candles
import pandas as pd
import ta

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    r = requests.post(url, params=params)
    return r.status_code == 200

def calculate_rsi(candles, window=14):
    # candles: lista de candles retornada pela Binance
    df = pd.DataFrame(candles, columns=[
        'open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
        'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
        'taker_buy_quote_asset_volume', 'ignore'
    ])

    df['close'] = pd.to_numeric(df['close'])
    rsi = ta.momentum.RSIIndicator(df['close'], window=window)
    df['rsi'] = rsi.rsi()
    return df

def generate_signal():
    candles = get_recent_candles()
    df = calculate_rsi(candles)

    last_rsi = df['rsi'].iloc[-1]

    if last_rsi < 30:
        signal = "📈 SINAL DE COMPRA: RSI está baixo ({:.2f}) — possível reversão!".format(last_rsi)
    elif last_rsi > 70:
        signal = "📉 SINAL DE VENDA: RSI está alto ({:.2f}) — possível correção!".format(last_rsi)
    else:
        signal = "⚪️ RSI neutro ({:.2f}) — sem sinal claro.".format(last_rsi)

    sent = send_telegram_message(signal)
    if sent:
        print("✅ Sinal enviado para o Telegram.")
    else:
        print("❌ Falha ao enviar o sinal.")

if __name__ == "__main__":
    generate_signal()
