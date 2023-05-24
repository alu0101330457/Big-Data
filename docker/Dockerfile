#FROM apache/airflow:2.0.2
# Actualiza la versión de Python a 3.8
FROM apache/airflow:latest-python3.8
COPY requirements.txt /requirements.txt

RUN pip install --user --upgrade pip


USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         build-essential libopenmpi-dev \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# Install git
RUN apt-get update && apt-get install -y git
RUN apt-get install libsasl2-dev


# Actualizar la lista de paquetes e instalar Java
RUN apt-get update && \
    apt-get install -y default-jdk && \
    rm -rf /var/lib/apt/lists/*

# Establecer la variable de entorno JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/default-java


USER airflow
RUN pip install apache-airflow[operators]
RUN pip install apache-airflow-providers-apache-spark
RUN pip install --no-cache-dir apache-airflow-providers-apache-hive
RUN pip install apache-airflow-providers-jdbc
RUN pip install --no-cache-dir --user -r /requirements.txt



#docker build . --tag extending_airflow:lastest

# docker compose up airflow-init