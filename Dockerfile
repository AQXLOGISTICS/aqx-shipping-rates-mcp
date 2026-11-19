FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml server.py README.md ./
RUN pip install --no-cache-dir mcp>=1.0.0 requests>=2.31.0

ENTRYPOINT ["python", "server.py"]
