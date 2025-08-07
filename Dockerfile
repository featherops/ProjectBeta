# Use a base image with Python
FROM python:3.9-slim

# Install Node.js and npm
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs

# Set the working directory
WORKDIR /app

# Copy all the files to the working directory
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r Ransomeware/requirements.txt

# Install Node.js dependencies and build the Next.js app
RUN cd app/app && npm install && npm run build

# Expose the port Hugging Face Spaces uses
EXPOSE 7860

# Create a startup script
RUN echo '#!/bin/bash' > /app/start.sh && \
    echo 'python3 api/server.py &' >> /app/start.sh && \
    echo 'cd app/app && npm start -- --port 7860' >> /app/start.sh && \
    chmod +x /app/start.sh

# Set the entrypoint to the startup script
CMD ["/app/start.sh"]
