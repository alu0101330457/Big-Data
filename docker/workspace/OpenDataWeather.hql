CREATE DATABASE IF NOT EXISTS open_weather_datadb
COMMENT 'This database contains information about weather of tenerife north airport';

USE open_weather_datadb;


DROP TABLE IF EXISTS weather;

CREATE EXTERNAL TABLE IF NOT EXISTS weather (
  Fecha TIMESTAMP,
  Temperatura_c DOUBLE,
  Velocidad_del_viento_km_h DOUBLE,
  Direccion_del_viento STRING,
  Racha_km_h DOUBLE,
  Direccion_de_racha STRING,
  Precipitacion_mm DOUBLE,
  Presion_hPa  DOUBLE,
  Tendencia_hPa DOUBLE,
  Humedad_percent DOUBLE

)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';


