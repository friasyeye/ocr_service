# Imagen oficial de Paddle (funciona con Python 3.7)
FROM paddlepaddle/paddle:2.5.2

# Instalamos dependencias del sistema necesarias para PDFs
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo
WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
