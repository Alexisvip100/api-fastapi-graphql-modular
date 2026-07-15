# Usa una imagen base oficial de Python ligera
FROM python:3.12-slim

# Evita que Python escriba archivos .pyc y asegura que la salida se envíe directamente a la consola
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Instala dependencias del sistema esenciales para PostgreSQL y compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación al contenedor
COPY . .

# Expone el puerto por defecto de FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación en modo desarrollo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
