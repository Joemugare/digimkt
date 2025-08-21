FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and core tools
RUN pip install --upgrade pip setuptools wheel setuptools_scm

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files (ignore .map to avoid Bootstrap issues)
RUN python manage.py collectstatic --noinput --ignore="*.map"

# Expose port
EXPOSE 8000

# Run migrations & start server
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn digital_marketing_blog.wsgi:application --bind 0.0.0.0:8000"]
