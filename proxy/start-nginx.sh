#!/bin/sh

# Substitute environment variables in the template and save to nginx.conf
envsubst '${BACKEND_HOST} ${BACKEND_PORT} ${STATIC_ROOT}' < /etc/nginx/nginx.dev.conf > /etc/nginx/nginx.conf

# Start Nginx
nginx -g 'daemon off;'
