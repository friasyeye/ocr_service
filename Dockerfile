# Imagen base de Paddle con Python y dependencias listas
FROM paddlepaddle/paddle:2.5.2

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo
WORKDIR /app

# Copiar e instalar dependencias Python (sin upgrade forzado de pip)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
