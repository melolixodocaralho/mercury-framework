FROM python:3.10-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir pytest

# This container is intended as an example sandbox for running plugin subprocesses
# in an isolated environment. Use with caution and only for authorized testing.

CMD ["python", "-c", "print('Mercury sandbox container ready')"]
