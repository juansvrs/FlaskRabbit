# Usa una imagen de Python como base
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los requisitos y la aplicación
COPY requirements.txt .
COPY app.py .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto donde Flask se ejecutará
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
