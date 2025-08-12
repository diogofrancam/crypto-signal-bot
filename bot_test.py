import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

mensagem = "🚀 Teste de conexão do bot de sinais - Está funcionando!"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
params = {"chat_id": CHAT_ID, "text": mensagem}

r = requests.post(url, params=params)

if r.status_code == 200:
    print("✅ Mensagem enviada com sucesso!")
else:
    print("❌ Erro ao enviar mensagem:", r.text)
