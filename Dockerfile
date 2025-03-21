# Use a smaller base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy only required files
COPY requirements.txt .

# Install dependencies with optimizations
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY main.py .

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Start the application
CMD ["python", "main.py"]

