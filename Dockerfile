# Use the official Python image as a base
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requisitos (si lo tienes) y luego instalar las dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente de tu proyecto al directorio de trabajo en el contenedor
COPY . .

# Exponer el puerto en el que se ejecutará tu aplicación
EXPOSE 8000

# Ejecutar el comando para iniciar tu aplicación FastAPI (cambiar 'main.py' por el nombre de tu archivo principal)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
