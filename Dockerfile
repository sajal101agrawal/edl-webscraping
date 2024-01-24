# Use an official Python runtime as a parent image
FROM python:3.11.7

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment and activate it
RUN python -m venv venv

RUN python -m pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN /app/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# Set the environment variable
ENV PORT=8765

# Make port 8765 available to the world outside this container
EXPOSE $PORT

# Run api.py when the container launches
CMD ["python", "websoket_fol/api.py"]
