# Usa la imagen oficial de Paddle con todo lo necesario a nivel sistema
FROM paddlepaddle/paddle:2.5.2

# Utilidades para PDF -> imagen
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependencias Python (forzamos opencv headless)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y opencv-python opencv-contrib-python || true

# Copia el código
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
