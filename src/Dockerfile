# Use a base image with Python 3.9.7
FROM python:3.9.7

# Install Node.js and npm
RUN apt-get update && apt-get install -y \
    nodejs \
    npm

# Install librsvg2-bin
RUN apt-get install -y librsvg2-bin && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install mathjax-node-cli
RUN npm install -g mathjax-node-cli

# Copy the requirements.txt file into the container
COPY requirements.txt /tmp/

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy your application into the container
COPY . /app
WORKDIR /app

# Set the default command for your container
#CMD ["python", "cli.py", "-d","-g", "-s", "-p"]
