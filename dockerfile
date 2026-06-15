# 1. Imagen base de python
FROM python:3.12-slim

# 2. Instalar dependecias del sistema para COLMAP, OpenCV y TKINTER (Interfaz Gráfica)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3-tk \
    colmap \
    && rm -rf /var/lib/apt/lists/*

# 3. Directorio de trabajo 
WORKDIR /app

# 4. Instalar dependencias limpias en python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copiar el código del proyecto
COPY . .

# 6. Ejecutar
CMD [ "python", "interfaz_grafica/main_pantalla.py" ]