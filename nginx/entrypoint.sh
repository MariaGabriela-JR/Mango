#!/bin/sh
if [ ! -f /etc/nginx/certs/fullchain.pem ] || [ ! -f /etc/nginx/certs/privkey.pem ]; then
  echo "Generating self-signed certificates..."
  mkdir -p /etc/nginx/certs
  openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout /etc/nginx/certs/privkey.pem \
    -out /etc/nginx/certs/fullchain.pem \
    -subj "/CN=localhost"
fi

echo "Aguardando gateway_app:8080..."
while ! nc -z gateway_app 8080; do
  sleep 2
done

echo "gateway_app disponível, iniciando Nginx..."
nginx -g "daemon off;"