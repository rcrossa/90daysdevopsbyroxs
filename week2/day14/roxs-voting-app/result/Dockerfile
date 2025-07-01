# Utiliza una imagen base oficial de Python
FROM ubuntu:22.04

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala Node.js
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Copia los archivos de requerimientos si existen
COPY ./package*.json /app/

# Instala las dependencias
RUN npm install --no-cache

COPY ./main.js /app/
COPY ./tests /app/tests
COPY ./views /app/views

# Comando por defecto para ejecutar el worker
CMD ["npm", "start"]