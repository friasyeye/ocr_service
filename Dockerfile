# Imagen base con Python 3.11
FROM python:3.11-slim

# Instalamos dependencias necesarias para PaddleOCR, pdf2image, OpenCV, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    poppler-utils \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo
WORKDIR /app

# Copiamos requirements.txt e instalamos dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
