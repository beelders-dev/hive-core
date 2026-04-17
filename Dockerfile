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

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]