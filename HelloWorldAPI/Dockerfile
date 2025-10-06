# Use Python 3.11 as base image
FROM python:3.11

# Add labels
LABEL version="1.0"
LABEL maintainer=""
LABEL description=""

# Set working directory
WORKDIR /usr/src/app

# Copy requirements file
COPY requirements.txt .

# Install dependencies without cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY . .

# Generate precompiled files (pycache)
RUN python -m compileall .

# Define entry point
CMD ["python", "HelloWorldAPI.py"]
