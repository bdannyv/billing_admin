FROM nginx:1.27.3-bookworm


# Install gettext to get envsubst
RUN apt-get update && apt-get install -y gettext-base && rm -rf /var/lib/apt/lists/*

# Copy the Nginx configuration template
COPY ./proxy/nginx.dev.conf /etc/nginx/nginx.dev.conf

# Copy the start script
COPY ./proxy/start-nginx.sh /start-nginx.sh

RUN groupadd -g 1000 nginxgroup && \
    useradd -r -u 1000 -g nginxgroup nginxuser

# Make the start script executable and accessible for the non-root user
RUN chmod +x /start-nginx.sh

# Define build arguments
ARG BACKEND_HOST
ARG BACKEND_PORT
ARG STATIC_ROOT

# Set environment variables
ENV BACKEND_HOST=${BACKEND_HOST}
ENV BACKEND_PORT=${BACKEND_PORT}
ENV STATIC_ROOT=${STATIC_ROOT}

# Create STATIC_ROOT that will be used for volume and grant access to nginxuser
RUN mkdir -p ${STATIC_ROOT} && chown -R nginxuser:nginxgroup ${STATIC_ROOT}

# Set the entrypoint to the start script
ENTRYPOINT ["/start-nginx.sh"]
