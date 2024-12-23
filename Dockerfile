FROM python:3.12.8-slim as base

# Install system dependencies and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry in a shared location
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
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

# Add a non-root user for security
RUN groupadd -g 1000 appgroup && \
    useradd -r -u 1000 -g appgroup appuser


COPY --chown=appuser:appgroup billing ./billing
COPY --chown=appuser:appgroup billing_admin ./billing_admin
COPY --chown=appuser:appgroup delegation ./delegation
COPY --chown=appuser:appgroup guidelines ./guidelines
COPY --chown=appuser:appgroup manage.py ./manage.py

USER appuser

FROM final as CI
COPY --from=CI-dep /usr/local /usr/local
RUN python manage.py migrate
CMD pytest .


# Production Stage
FROM final as PROD
COPY --from=PROD-dep /usr/local /usr/local
EXPOSE 8000
CMD ["gunicorn", "billing_admin.wsgi:application", "--bind", "0.0.0.0:8000"]
