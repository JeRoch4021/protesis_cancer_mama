# syntax=docker/dockerfile:1

# 1. Imagen base de python
FROM python:3.11-slim

# 2. Evitar que Linux se quede trabajando esperando selección de zona horaria
ENV DEBIAN_FRONTEND=noninteractive

# 3. Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 4. Definimos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# 5. Instalar dependencias limpias en python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Mantener el contenedor vivo en segundo plano esperando los comandos
CMD ["tail", "-f", "/dev/null"]