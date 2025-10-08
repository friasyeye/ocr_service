# Imagen base con Paddle (incluye Python)
FROM paddlepaddle/paddle:2.5.2

# Actualizar pip y librerías básicas del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip setuptools wheel

# Carpeta de trabajo
WORKDIR /app

# Instalar dependencias directamente (flask incluido)
RUN pip install flask paddleocr pdf2image Pillow numpy opencv-python-headless

# Copiar el proyecto (app.py, requirements.txt, etc.)
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
