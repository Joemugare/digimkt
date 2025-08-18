# Use official Python 3.12 slim image (compatible with Django 4.1)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for psycopg2, Pillow, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip, setuptools, wheel, and setuptools_scm first
RUN pip install --upgrade pip setuptools wheel setuptools_scm

# Copy requirements and install project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files (optional, uncomment if needed)
# RUN python manage.py collectstatic --noinput

# Expose port (Render uses PORT environment variable)
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "digital_marketing_blog.wsgi:application", "--bind", "0.0.0.0:8000"]

