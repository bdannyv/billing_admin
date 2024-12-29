FROM python:3.12.8-slim as base

# Install system dependencies and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry in a shared location
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./


# CI Dependencies Stage
FROM base as CI-dep
RUN poetry config virtualenvs.create false \
    && poetry install --with dev

# Production Dependencies Stage
FROM base as PROD-dep
RUN poetry config virtualenvs.create false \
    && poetry install --without dev


# CI Stage
FROM python:3.12.8-slim as final

ARG STATIC_ROOT
ARG DB_ENGINE
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT

ENV STATIC_ROOT=${STATIC_ROOT}
ENV DB_ENGINE=${DB_ENGINE}
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}

WORKDIR /app

# Add a non-root user for security
RUN groupadd -g 1000 appgroup && \
    useradd -r -u 1000 -g appgroup appuser


COPY billing ./billing
COPY billing_admin ./billing_admin
COPY delegation ./delegation
COPY guidelines ./guidelines
COPY manage.py ./manage.py

# grant read and write permissions to appuser to project root
RUN chown -R appuser:appgroup /app


FROM final as CI
COPY --from=CI-dep /usr/local /usr/local

# migrate the database
RUN python manage.py migrate

USER appuser
CMD ["python", "manage.py", "migrate;", "pytest ." ]


# Production Stage
FROM final as PROD

COPY --from=PROD-dep /usr/local /usr/local
# create dir for static files and grant permissions to appuser
RUN mkdir -p ${STATIC_ROOT} && chown -R appuser:appgroup ${STATIC_ROOT}
RUN python manage.py collectstatic --noinput

# run the server as appuser
USER appuser

CMD python manage.py migrate; gunicorn billing_admin.wsgi:application --bind 0.0.0.0:8000
