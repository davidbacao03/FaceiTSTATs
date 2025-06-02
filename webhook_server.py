import os
import hmac
import hashlib
import requests
from flask import Flask, request, abort

app = Flask(__name__)

# Defina o mesmo secret que você colocar na FACEIT ao criar o webhook
FACEIT_WEBHOOK_SECRET = os.getenv("FACEIT_WEBHOOK_SECRET", "sua_chave_secreta")
FACEIT_HEADER_NAME = "Faceits"
FACEIT_HEADER_VALUE = "my-secret-token"  # Troque para o valor que você definir na FACEIT
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1379210103408038002/owSXbndDQBGhaX2vJ59mX_Z6xD3GXdXHcR3Cm55bgcoPY47eLJeN3r-eaYXWI04fioFG"

@app.route("/faceit-webhook", methods=["POST"])
def faceit_webhook():
    # Validação de assinatura (se configurado na FACEIT)
    signature = request.headers.get("X-Signature")
    if FACEIT_WEBHOOK_SECRET and signature:
        computed = hmac.new(
            FACEIT_WEBHOOK_SECRET.encode(),
            request.data,
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(computed, signature):
            abort(401, "Invalid signature")
    
    # Validação do header de segurança
    if request.headers.get(FACEIT_HEADER_NAME) != FACEIT_HEADER_VALUE:
        abort(401, "Invalid security header")
    
    # Processa o evento recebido
    event = request.json
    print("Evento recebido da FACEIT:", event)
    
    # Envia mensagem para Discord Webhook
    msg = f"Evento FACEIT recebido: {event}"
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": msg})
    except Exception as e:
        print("Erro ao enviar para Discord Webhook:", e)
    
    return "ok", 200

if __name__ == "__main__":
    app.run(port=5000)