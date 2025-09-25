import asyncio
import aio_pika
import os

async def test_connections():
    # Testar RabbitMQ
    try:
        connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
        print("✅ Conectado ao RabbitMQ")
        
        channel = await connection.channel()
        queue = await channel.declare_queue("patients", durable=True, passive=True)
        print(f"✅ Fila 'patients' existe com {queue.declaration_result.message_count} mensagens")
        
        await connection.close()
    except Exception as e:
        print(f"❌ Erro RabbitMQ: {e}")
    
    # Testar FastAPI
    import httpx
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://fastapi_app:8001/fastapi/health")
            print(f"✅ FastAPI respondendo: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro FastAPI: {e}")

if __name__ == "__main__":
    asyncio.run(test_connections())