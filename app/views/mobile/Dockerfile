FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    build-essential \
    git \
    python3 \
    python3-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Set display environment variable
ENV DISPLAY=host.docker.internal:0.0

COPY requirements.txt .

# Install Kivy dependencies first
RUN pip install --no-cache-dir kivy_deps.sdl2==0.8.0 \
    kivy_deps.glew==0.3.1 \
    kivy_deps.gstreamer==0.3.3

# Then install the rest of the requirements
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app/views/mobile/main.py"] 