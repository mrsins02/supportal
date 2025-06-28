FROM python:3.10 AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/root/.local/bin:$PATH"

# Install build dependencies
RUN apt update && apt install -y gettext curl build-essential

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --with dev

# Copy app files
COPY . .

# ---------- Stage 2: Final Runtime Stage ----------
FROM python:3.10

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set environments
ARG POSTGRES_HOST
ARG MYSQL_PORT
ENV POSTGRES_HOST=${POSTGRES_HOST}
ENV POSTGRES_PORT=${POSTGRES_PORT}
ENV DJANGO_SETTINGS_MODULE=config.settings

# Install required runtime packages
RUN apt update && apt install -y gettext curl

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /app /app

# Get wait-for-it script
RUN curl -o /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
 && chmod +x /usr/local/bin/wait-for-it.sh

# Set entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Collect static files (optional)
RUN python3 manage.py collectstatic --noinput
# RUN python3 manage.py compilemessages

ENTRYPOINT ["/entrypoint.sh"]
