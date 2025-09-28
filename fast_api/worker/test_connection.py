import asyncio
import aio_pika
import os

async def test_connections():
    # Testar RabbitMQ
    try:
        connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
        print("Connected to RabbitMQ")
        
        channel = await connection.channel()
        queue = await channel.declare_queue("patients", durable=True, passive=True)
        print(f"Queue 'patients' exists with {queue.declaration_result.message_count} messages")
        
        await connection.close()
    except Exception as e:
        print(f"Error in RabbitMQ: {e}")
    
    # Testar FastAPI
    import httpx
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://fastapi_app:8001/fastapi/health")
            print(f"FastAPI answering: {response.status_code}")
    except Exception as e:
        print(f"Error in FastAPI: {e}")

if __name__ == "__main__":
    asyncio.run(test_connections())