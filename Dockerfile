# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment and activate it
RUN python -m venv venv && \
    chmod +x /app/venv/bin/activate

# Upgrade Pip
RUN /app/venv/bin/pip install --upgrade pip

# Install dependencies from requirements.txt
RUN /app/venv/bin/pip install --no-cache-dir -r /app/requirements.txt


# Set the environment variable
ENV PORT=8765

# Expose port 8765 to the world outside this container
EXPOSE $PORT

# Activate virtual environment and run api.py when the container launches
CMD ["/bin/bash", "-c", "source /app/venv/bin/activate && exec /app/venv/bin/python /app/websoket_fol/api.py"]

