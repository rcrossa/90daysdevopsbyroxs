FROM ubuntu:22.04

# Instala dependencias del sistema y Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia archivos en el orden correcto
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/
COPY tests/ tests/

EXPOSE 5000

CMD ["python3", "app.py"]
