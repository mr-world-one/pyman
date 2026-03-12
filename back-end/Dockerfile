FROM python:3.11-slim

# System deps: Chromium for Selenium, Ghostscript for camelot-py, OCR tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    xdg-utils \
    wget \
    curl \
    ghostscript \
    libgs-dev \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-ukr \
    tesseract-ocr-eng \
    libffi-dev \
    libpq-dev \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Chrome / Selenium env vars
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV DISPLAY=:99

WORKDIR /app

# Copy and install backend dependencies
COPY back-end/requirements.txt /tmp/backend-requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/backend-requirements.txt

# Install camelot-py (PDF table extraction) + its CV backend + PyMuPDF (fitz) + ocrmypdf
RUN pip install --no-cache-dir \
    "camelot-py[cv]" \
    opencv-python-headless \
    PyMuPDF \
    ocrmypdf

# Install scraper deps (psycopg2-binary for Docker, selenium, etc.)
RUN pip install --no-cache-dir selenium webdriver-manager psycopg2-binary

# Install additional packages needed for async DB and Excel parsing
RUN pip install --no-cache-dir "sqlalchemy[asyncio]" asyncpg python-dotenv openpyxl pandas

# Ensure email-validator is present (pydantic[email] needs it)
RUN pip install --no-cache-dir email-validator

# Google Gemini API for LLM-based product validation
RUN pip install --no-cache-dir google-generativeai

# Copy source code
COPY back-end/ /app/back-end/
COPY scraper/ /app/scraper/

# Add project root + back-end to PYTHONPATH
ENV PYTHONPATH=/app:/app/back-end

WORKDIR /app/back-end

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
