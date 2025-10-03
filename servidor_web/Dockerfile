# Use the official Python 3.8 slim image as the base image
FROM python:3.10-slim

# Set the working directory within the container
WORKDIR /app

# Install 
RUN apt-get update && apt-get install -y libpq-dev gcc && apt-get clean

# Copy the necessary files and directories into the container
COPY main_server.py requirements.txt wsgi.py  /app/
COPY templates/*  /app/templates/

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask application
EXPOSE 5000

# Execute command: gunicorn wsgi -b 0.0.0.0:5000
CMD ["gunicorn", "wsgi", "-b", "0.0.0.0:5000", "-w", "4"]

