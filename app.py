from twilio.rest import Client
import random
from datetime import datetime
import os
# 🔑 SUAS CREDENCIAIS


account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')

client = Client(account_sid, auth_token)

jogos = [
    {"jogo": "Flamengo x Bahia", "mercado": "Over 1.5 gols", "odd": 1.35},
    {"jogo": "Palmeiras x Cuiabá", "mercado": "Palmeiras vence", "odd": 1.50},
    {"jogo": "Real Madrid x Getafe", "mercado": "Over 2.5 gols", "odd": 1.60},
    {"jogo": "PSG x Nantes", "mercado": "PSG vence + Over 1.5", "odd": 1.55},
    {"jogo": "Liverpool x Everton", "mercado": "Over 2.5 gols", "odd": 1.60},
]

def enviar_whatsapp():
    print("➡️ Entrou na função enviar_whatsapp")

    try:
        selecoes = random.sample(jogos, 3)
        odd_total = 1

        mensagem = f"📅 {datetime.now().strftime('%d/%m/%Y')}\n"
        mensagem += "🎯 Aposta do Dia:\n\n"

        for s in selecoes:
            mensagem += f"{s['jogo']} - {s['mercado']} (odd {s['odd']})\n"
            odd_total *= s["odd"]

        mensagem += f"\n🔥 Odd Total: {round(odd_total,2)}"
        mensagem += "\n💰 Stake: 5% da banca"

        print("📤 Enviando mensagem...")

        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=mensagem,
            to='whatsapp:+55SEUNUMERO'
        )

        print("✅ Mensagem enviada! SID:", message.sid)

    except Exception as e:
        print("❌ ERRO AO ENVIAR:", e)
        

# =========================
# PARTE DO RENDER (NÃO APAGAR)
# =========================

from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Robô rodando!"

def run_bot():
    import schedule
    import time

    print("🔥 ROBÔ INICIADO")

    try:
        print("📲 Tentando enviar mensagem...")
        enviar_whatsapp()
    except Exception as e:
        print("❌ ERRO AO ENVIAR:", e)

    schedule.every().day.at("10:00").do(enviar_whatsapp)

    while True:
        schedule.run_pending()
        time.sleep(60)

# 🔥 ESSA LINHA É A CHAVE
import threading
import os

def start_bot():
    print("🔥 ROBÔ INICIADO")
    run_bot()

if __name__ == "__main__":
    print("🚀 Iniciando robô...")

    thread = threading.Thread(target=start_bot)
    thread.daemon = True
    thread.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
