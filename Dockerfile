# Use the slim version of Python 3.12 as the base image
FROM python:3.12-slim

# Set environment variables to reduce the size of the image
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock /app/

# Install pipenv and the dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        build-essential && \
    pip install --no-cache-dir pipenv && \
    pipenv install --deploy --system && \
    apt-get purge -y --auto-remove gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy the bot script to the working directory
COPY skyprice_bot.py /app/

# Command to run the bot
CMD ["python", "skyprice_bot.py"]
