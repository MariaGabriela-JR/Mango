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
    """Gets or creates a connection and channel with RabbitMQ"""
    global _connection, _channel
    
    if _channel is None or _channel.is_closed:
        if _connection is not None:
            await _connection.close()
        
        _connection = await aio_pika.connect_robust(RABBIT_URL)
        _channel = await _connection.channel()
        await _channel.declare_queue(QUEUE_NAME, durable=True)
        print(f"[Publisher] Connection established with RabbitMQ")
    
    return _channel

async def publish_patient(patient_data: dict):
    """
    Publishes a JSON message to RabbitMQ.
    """
    if not patient_data:
        print("[Publisher] Empty data, message will not be sent.")
        return

    try:
        message_body = json.dumps(patient_data).encode()
    except (TypeError, ValueError) as e:
        print(f"[Publisher] Error converting data to JSON: {e}")
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
        print(f"[Publisher] Message sent to queue '{QUEUE_NAME}': {patient_data}")
        
    except Exception as e:
        print(f"[Publisher] Error sending to RabbitMQ: {e}")
        global _connection, _channel
        _connection = None
        _channel = None

def send_to_worker(patient_data: dict):
    """
    Synchronous function that can be called in views.
    """
    asyncio.run(publish_patient(patient_data))

async def close_connection():
    """Closes the connection (useful for shutdown)"""
    global _connection, _channel
    if _connection:
        await _connection.close()
        _connection = None
        _channel = None