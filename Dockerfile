FROM python:3.12-slim

WORKDIR /app

# Install git and build essentials if needed (usually not for pure python, but good to have)
# RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install dependencies and the package
RUN pip install --no-cache-dir .

# Expose port
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# Create a non-root user
# Use a numeric UID to make it compatible with Kubernetes security contexts
RUN useradd -m -u 1000 appuser

# Switch to non-root user
USER appuser

# Entrypoint
# We use the script installed by pyproject.toml which now points to mcp_server_kibana.server:main
ENTRYPOINT ["mcp-server-kibana"]
CMD ["http"]