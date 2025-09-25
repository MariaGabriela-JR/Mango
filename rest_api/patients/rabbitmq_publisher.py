import aio_pika
import asyncio
import json
import os

RABBIT_URL = os.getenv("RABBIT_URL", "amqp://guest:guest@rabbitmq/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "patients")

# Cache de conexão e canal
_connection = None
_channel = None

async def get_rabbitmq_channel():
    """Obtém ou cria uma conexão e canal com RabbitMQ"""
    global _connection, _channel
    
    if _channel is None or _channel.is_closed:
        if _connection is not None:
            await _connection.close()
        
        _connection = await aio_pika.connect_robust(RABBIT_URL)
        _channel = await _connection.channel()
        await _channel.declare_queue(QUEUE_NAME, durable=True)
        print(f"[Publisher] Conexão com RabbitMQ estabelecida")
    
    return _channel

async def publish_patient(patient_data: dict):
    """
    Publica uma mensagem JSON no RabbitMQ.
    """
    if not patient_data:
        print("[Publisher] Dados vazios, mensagem não será enviada.")
        return

    try:
        # Converte para JSON
        message_body = json.dumps(patient_data).encode()
    except (TypeError, ValueError) as e:
        print(f"[Publisher] Erro ao converter dados para JSON: {e}")
        return

    try:
        channel = await get_rabbitmq_channel()
        
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message_body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=QUEUE_NAME
        )
        print(f"[Publisher] Mensagem enviada para a fila '{QUEUE_NAME}': {patient_data}")
        
    except Exception as e:
        print(f"[Publisher] Erro ao enviar para RabbitMQ: {e}")
        # Reseta a conexão em caso de erro
        global _connection, _channel
        _connection = None
        _channel = None

def send_to_worker(patient_data: dict):
    """
    Função síncrona que pode ser chamada nas views.
    """
    asyncio.run(publish_patient(patient_data))

async def close_connection():
    """Fecha a conexão (útil para shutdown)"""
    global _connection, _channel
    if _connection:
        await _connection.close()
        _connection = None
        _channel = None