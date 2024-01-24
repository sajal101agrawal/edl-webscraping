# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment and activate it
RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate"

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable
ENV PORT=8765

# Make port 8765 available to the world outside this container
EXPOSE $PORT

# Run api.py when the container launches
CMD ["python", "websoket_fol/api.py"]
