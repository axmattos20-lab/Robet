from flask import Flask
from twilio.rest import Client
import os
import schedule
import time
from threading import Thread

# ===============================
# CONFIGURAÇÃO TWILIO
# ===============================
account_sid = os.environ.get('ACCOUNT_SID')  # do Render Environment Variables
auth_token = os.environ.get('AUTH_TOKEN')    # do Render Environment Variables
client = Client(account_sid, auth_token)

# ===============================
# FUNÇÃO DE ENVIO DE MENSAGEM
# ===============================
def enviar_whatsapp():
    mensagem = "📅 Aposta do Dia:\nJogo X - Mercado Y (Odd 1.80)\n🔥 Odd Total: 1.80"
    to = 'whatsapp:+5521973824229'  # substitua pelo seu número com DDD
    
    try:
        print("➡️ Tentando enviar mensagem...")
        message = client.messages.create(
            from_='whatsapp:+14155238886',  # Twilio Sandbox
            body=mensagem,
            to=to
        )
        print("✅ Mensagem enviada! SID:", message.sid)
    except Exception as e:
        print("❌ ERRO REAL DO TWILIO:", e)

# ===============================
# AGENDAMENTO DIÁRIO
# ===============================
def enviar_diariamente():
    enviar_whatsapp()

# Envia todos os dias às 10:00 AM
schedule.every().day.at("22:00").do(enviar_diariamente)

def rodar_agenda():
    while True:
        schedule.run_pending()
        time.sleep(60)  # checa a cada minuto

# Inicia a thread da agenda
Thread(target=rodar_agenda).start()

# ===============================
# FLASK PARA MANTER RENDER ATIVO
# ===============================
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Robô de Apostas Ativo!"

if __name__ == '__main__':
    # Porta padrão 10000 ou a definida no Render
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
