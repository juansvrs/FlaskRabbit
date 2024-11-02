from flask import Flask, request, jsonify
from flask_cors import CORS
import pika
import json
import time

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

# Conexión a RabbitMQ con reintentos
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        break  # Sale del bucle si la conexión es exitosa
    except pika.exceptions.AMQPConnectionError:
        print("Esperando a que RabbitMQ esté disponible...")
        time.sleep(1)  # Espera 1 segundo antes de reintentar

# Declara la cola por defecto
channel.queue_declare(queue='queue')

@app.route('/mensajes', methods=['POST'])
def enviar_mensaje():
    mensaje = request.json  # Obtiene el mensaje del cuerpo de la solicitud
    channel.basic_publish(exchange='', routing_key='queue', body=json.dumps(mensaje))
    return jsonify({"mensaje": "Mensaje enviado"}), 200

@app.route('/mensajes', methods=['GET'])
def obtener_mensajes():
    mensajes = []
    while True:
        method_frame, header_frame, body = channel.basic_get('queue')
        if method_frame:
            mensajes.append(json.loads(body))
            channel.basic_ack(method_frame.delivery_tag)  # Confirma que el mensaje fue recibido
        else:
            break
    return jsonify(mensajes), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
