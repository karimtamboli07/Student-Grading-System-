# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.12.0b1-slim-buster 

# Set the working directory in the container to /app
WORKDIR /app

# Install build dependencies for mysqlclient
RUN apt-get update && \
    apt-get install -y --no-install-recommends pkg-config 

# Copy the requirements file into the container at /app
COPY requirements.txt ./

# Copy the entire application code into the container at /app
COPY . ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to the outside world (Flask default port)
EXPOSE 5000

# Define the command to run your Flask application
CMD ["python", "-m", "report_card_system.app"]
