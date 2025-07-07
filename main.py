from flask import Flask, request, redirect
import requests
import os

app = Flask(__name__)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

@app.route('/')
def home():
    return "Servidor de pagos activo."

@app.route('/pagar', methods=['GET'])
def pagar():
    monto = request.args.get('monto', type=float)
    if not monto or monto <= 0:
        return "Monto no válido", 400

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    data = {
        "items": [{
            "title": "Pago por servicio audiovisual",
            "quantity": 1,
            "currency_id": "CLP",
            "unit_price": monto
        }],
        "back_urls": {
            "success": "https://veriteproducciones.cl/gracias",
            "failure": "https://veriteproducciones.cl/error",
            "pending": "https://veriteproducciones.cl/pendiente"
        },
        "auto_return": "approved"
    }

    response = requests.post(
        "https://api.mercadopago.com/checkout/preferences",
        headers=headers,
        json=data
    )

    if response.status_code != 201:
        return f"Error al crear preferencia: {response.text}", 500

    link_pago = response.json()["init_point"]
    return redirect(link_pago)

if __name__ == "__main__":
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
