#!/bin/bash
set -e

echo "Aguardando o banco de dados ficar pronto..."
# Espera o banco de dados estar disponível
while ! nc -z db_fastapi 5432; do
  sleep 2
done
echo "Banco de dados pronto!"

echo "Executando migrações do Alembic..."
alembic upgrade head

echo "Iniciando aplicação FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
