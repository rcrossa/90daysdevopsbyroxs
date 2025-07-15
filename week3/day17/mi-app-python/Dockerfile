FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instala Python y dependencias
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
COPY app.py .

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Usuario no root
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["python3", "app.py"]