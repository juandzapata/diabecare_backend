# Usa una imagen base que incluya Python
FROM python:3.11

# Actualiza pip y setuptools
RUN pip install --upgrade pip setuptools

# Instala los paquetes necesarios para el controlador ODBC de SQL Server
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

#instala git

# Instala el controlador ODBC de SQL Server 18 para Linux
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Configura el entorno de Python
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de tu aplicación
COPY . .

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Exponer el puerto que utiliza tu aplicación FastAPI
EXPOSE 8000

# Comando para iniciar la aplicación FastAPI
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]