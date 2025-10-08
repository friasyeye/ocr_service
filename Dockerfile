# Usa la imagen oficial de Paddle con todo lo necesario a nivel sistema
FROM paddlepaddle/paddle:2.5.2

# Instala utilidades necesarias para PDF -> imagen
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo
WORKDIR /app

# Copiamos requirements.txt desde la carpeta correcta
COPY ocr_service/requirements.txt ./requirements.txt

# Instalamos dependencias Python (forzamos opencv headless)
RUN pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y opencv-python opencv-contrib-python || true

# Copiamos el resto del código de la carpeta ocr_service
COPY ocr_service/ .

EXPOSE 5000
CMD ["python", "app.py"]
