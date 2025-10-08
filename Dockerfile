# Imagen base con Paddle (incluye Python y dependencias básicas)
FROM paddlepaddle/paddle:2.5.2

# Dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y opencv-python opencv-contrib-python || true

# Copiar el resto del código
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
