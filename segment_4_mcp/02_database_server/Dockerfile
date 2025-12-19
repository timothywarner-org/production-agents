FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install mcp aiosqlite

# Copy server code
COPY server.py .

# Create data directory
RUN mkdir -p /data
ENV DATABASE_PATH=/data/demo.db

# Run server
CMD ["python", "server.py"]
