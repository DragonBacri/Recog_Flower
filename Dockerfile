# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables for production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set the working directory in the container
WORKDIR /app


# Copy requirements.txt and install dependencies first to leverage Docker layer caching
COPY requirements.txt ./
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#Copy the rest of the app
COPY . .



# Use Gunicorn, a production-grade WSGI server.
# Cloud Run automatically sets the PORT environment variable and sends traffic to port 8080.
# The target 'app.app:app' means: in the 'app' directory, find the 'app.py' file, and inside it, use the Flask object named 'app'.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "app.app:app"]
