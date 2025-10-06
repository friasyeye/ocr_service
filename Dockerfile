# Imagen base con Python 3.11
FROM python:3.11-slim

# Instalamos dependencias del sistema necesarias para Tesseract y fuentes
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    tesseract-ocr-cat \
    libtesseract-dev \
    poppler-utils \
    && apt-get clean

# Creamos carpeta de trabajo
WORKDIR /app

# Copiamos los archivos del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
