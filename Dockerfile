FROM python:3.12-slim

# Keep the logs clean and the engine fast
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# The "Pro" step the book missed: Prepare for Postgres
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# The "Caching" step: Install libs first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# The "Final" step: Copy your code
COPY . .



RUN SECRET_KEY="django-insecure-build-key" \
    POSTGRES_DB="build" \
    POSTGRES_USER="build" \
    POSTGRES_PASSWORD="build" \
    POSTGRES_HOST="localhost" \
    POSTGRES_PORT="5432" \
    python manage.py collectstatic --noinput

EXPOSE 8080

CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:$PORT"]