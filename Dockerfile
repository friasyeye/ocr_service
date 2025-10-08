# Imagen base con Python 3.11
FROM python:3.11-slim

# Instalamos dependencias del sistema necesarias para pdf2image
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && apt-get clean

# Carpeta de trabajo
WORKDIR /app

# Copiamos e instalamos dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de archivos del proyecto
COPY . .

# Exponemos el puerto 5000
EXPOSE 5000

# Comando por defecto
CMD ["python", "app.py"]

