FROM nginx:alpine
RUN apk add --no-cache openssl
COPY conf.d /etc/nginx/conf.d
COPY certs /etc/nginx/certs
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
