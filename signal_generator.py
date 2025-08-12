import os
from dotenv import load_dotenv
import requests
from binance_client import get_recent_candles
import pandas as pd
import ta
from datetime import datetime, date
import json

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Parâmetros do robô
MAX_OPS_PER_DAY = 10
DAILY_TARGET_USD = 100
DAILY_MAX_LOSS_USD = 50
INITIAL_CAPITAL_USD = 200
LEVERAGE = 15

# Arquivo para controle simples do número de sinais por dia
OPS_COUNTER_FILE = "ops_counter.json"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    r = requests.post(url, params=params)
    return r.status_code == 200

def load_ops_counter():
    try:
        with open(OPS_COUNTER_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {"date": str(date.today()), "count": 0}
    return data

def save_ops_counter(data):
    with open(OPS_COUNTER_FILE, "w") as f:
        json.dump(data, f)

def increment_ops_counter():
    data = load_ops_counter()
    today_str = str(date.today())
    if data.get("date") != today_str:
        data = {"date": today_str, "count": 0}
    data["count"] += 1
    save_ops_counter(data)
    return data["count"]

def calculate_indicators(candles):
    df = pd.DataFrame(candles, columns=[
        'open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
        'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
        'taker_buy_quote_asset_volume', 'ignore'
    ])

    df['close'] = pd.to_numeric(df['close'])
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])

    # RSI com janela menor para mais sensibilidade
    rsi = ta.momentum.RSIIndicator(df['close'], window=9)
    df['rsi'] = rsi.rsi()

    # Médias móveis exponenciais mais rápidas para detectar tendências curtas
    ema9 = ta.trend.EMAIndicator(df['close'], window=9)
    ema21 = ta.trend.EMAIndicator(df['close'], window=21)
    df['ema9'] = ema9.ema_indicator()
    df['ema21'] = ema21.ema_indicator()

    # ATR para volatilidade
    atr = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close'], window=14)
    df['atr'] = atr.average_true_range()

    return df

def define_levels(last, df):
    # Níveis simples baseados em candles anteriores e ATR
    atr = last['atr']
    close = last['close']

    # Stop Loss a 0.7x ATR do preço de entrada
    stop_loss = close - 0.7 * atr

    # Take Profit a 1.5x ATR do preço de entrada
    take_profit = close + 1.5 * atr

    # Garantir stop_loss positivo e menor que close
    if stop_loss < 0 or stop_loss >= close:
        stop_loss = close * 0.98  # 2% stop fixo se cálculo falhar

    return stop_loss, take_profit

def generate_signal():
    # Controle de operações por dia
    ops_data = load_ops_counter()
    if ops_data["count"] >= MAX_OPS_PER_DAY:
        print("⚠️ Limite diário de operações atingido.")
        return

    candles = get_recent_candles(limit=100)
    df = calculate_indicators(candles)
    last = df.iloc[-1]

    rsi = last['rsi']
    ema9 = last['ema9']
    ema21 = last['ema21']
    close = last['close']
    atr = last['atr']

    # Debug prints
    print(f"RSI: {rsi:.2f}, EMA9: {ema9:.2f}, EMA21: {ema21:.2f}, Close: {close:.4f}, ATR: {atr:.4f}")

    signal = ""

    # Condições mais agressivas para gerar mais sinais
    is_bull = ema9 > ema21 and rsi < 50
    is_bear = ema9 < ema21 and rsi > 50

    if is_bull:
        stop_loss, take_profit = define_levels(last, df)
        signal += (
            f"🚀 SINAL DE COMPRA\n"
            f"Preço: {close:.4f}\n"
            f"Stop Loss: {stop_loss:.4f}\n"
            f"Take Profit: {take_profit:.4f}\n"
            f"Alavancagem: {LEVERAGE}x\n"
            f"Meta diária: {DAILY_TARGET_USD} USD\n"
            f"Stop máximo diário: {DAILY_MAX_LOSS_USD} USD\n"
            f"⚠️ Risco calculado para capital inicial de {INITIAL_CAPITAL_USD} USD\n"
            f"💡 Use gestão de risco e confirme sempre com análise gráfica."
        )
        increment_ops_counter()
    elif is_bear:
        stop_loss, take_profit = define_levels(last, df)
        # Ajusta níveis para venda (inverte Stop e TP)
        stop_loss_sell = close + (close - stop_loss)
        take_profit_sell = close - (take_profit - close)
        signal += (
            f"🛑 SINAL DE VENDA\n"
            f"Preço: {close:.4f}\n"
            f"Stop Loss: {stop_loss_sell:.4f}\n"
            f"Take Profit: {take_profit_sell:.4f}\n"
            f"Alavancagem: {LEVERAGE}x\n"
            f"Meta diária: {DAILY_TARGET_USD} USD\n"
            f"Stop máximo diário: {DAILY_MAX_LOSS_USD} USD\n"
            f"⚠️ Risco calculado para capital inicial de {INITIAL_CAPITAL_USD} USD\n"
            f"💡 Use gestão de risco e confirme sempre com análise gráfica."
        )
        increment_ops_counter()
    else:
        signal += (
            f"⚪️ SEM SINAL CLARO\n"
            f"RSI: {rsi:.2f}, EMA9: {ema9:.2f}, EMA21: {ema21:.2f}\n"
            f"Aguardando condições melhores."
        )

    sent = send_telegram_message(signal)
    if sent:
        print("✅ Sinal enviado para o Telegram.")
    else:
        print("❌ Falha ao enviar o sinal.")

if __name__ == "__main__":
    generate_signal()
