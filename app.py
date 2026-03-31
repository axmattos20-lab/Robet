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
    selecoes = random.sample(jogos, 3)
    odd_total = 1

    mensagem = f"📅 {datetime.now().strftime('%d/%m/%Y')}\n"
    mensagem += "🎯 Aposta do Dia:\n\n"

    for s in selecoes:
        mensagem += f"{s['jogo']} - {s['mercado']} (odd {s['odd']})\n"
        odd_total *= s["odd"]

    mensagem += f"\n🔥 Odd Total: {round(odd_total,2)}"
    mensagem += "\n💰 Stake: 5% da banca"

    client.messages.create(
        from_='whatsapp:+14155238886',
        body=mensagem,
        to='whatsapp:+5521973824229'
    )

    print("Mensagem enviada!")

        # 🔥 TESTE TEMPORÁRIO (coloque aqui)
        enviar_whatsapp()

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
    # 🔥 TESTE TEMPORÁRIO (coloque aqui)
        enviar_whatsapp()

    schedule.every().day.at("10:00").do(enviar_whatsapp)

    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=run_bot).start()

app.run(host='0.0.0.0', port=10000)
