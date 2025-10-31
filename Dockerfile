# Use Python base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy requirement file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python", "-m", "app"]
