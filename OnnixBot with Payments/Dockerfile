# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files
COPY ENHANCED_POCKET_OPTION_BOT.py .
COPY .env .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash bot
USER bot

# Run the bot
CMD ["python", "ENHANCED_POCKET_OPTION_BOT.py"]