# Use lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy all files (including dashboard)
COPY . .

# Install main and dashboard dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r weather-dashboard/requirements.txt

# Expose the Flask app port
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start the dashboard app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "weather-dashboard.app:app"]
