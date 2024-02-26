# Use the official Python image for ARM architecture from the Docker Hub
FROM arm32v7/python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Install Google Chrome for ARM architecture
RUN apt-get update && \
    apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_armhf.deb && \
    apt install -y ./google-chrome-stable_current_armhf.deb && \
    rm google-chrome-stable_current_armhf.deb && \
    apt-get clean

# Expose the WebSocket port
EXPOSE 8765

# Run the WebSocket server when the container starts
CMD ["python3", "websoket_fol/api.py"]
