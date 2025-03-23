# Use a slim Python image for efficiency
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies first (optimizes caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose port (Render will map this to an external port)
EXPOSE 5000

# Use Gunicorn to run the app, binding to 0.0.0.0 and a dynamic port
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.routes:app"]