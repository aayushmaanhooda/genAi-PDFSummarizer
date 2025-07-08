# Use an official Python runtime as a parent image
FROM python:3.10-slim



# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose Streamlit port
EXPOSE 8501


# Command to run your app
CMD ["streamlit", "run", "main.py"]
