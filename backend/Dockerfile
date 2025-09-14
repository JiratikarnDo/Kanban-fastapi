FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy all files from the current directory (the build context) to /app
COPY . /app

# Set the Python path
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]