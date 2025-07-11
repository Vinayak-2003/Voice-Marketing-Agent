# backend/Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Prevent python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure python output is sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for Coqui TTS and audio processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    espeak-ng \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend source code into the container
COPY . .

# Create a directory for audio files that will be generated
RUN mkdir -p /app/audio_files

# The command to run the application using Uvicorn
# It will be run from the docker-compose file to allow for --reload flag
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]