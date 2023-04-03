
from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.operators.python_operator import PythonOperator
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType
from pyspark.sql.functions import to_timestamp
from pyspark.sql.functions import col




import requests
import pandas as pd
import numpy as np






default_args = {
    'owner' : 'Mario',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

@dag(dag_id='dag_weather_etl_v02',
     default_args=default_args,
     start_date=datetime(2023, 4, 1),
     schedule_interval= '@daily')
def weather_etl():
    
        
    
    @task
    def process_data():
        
        spark = SparkSession\
        .builder\
        .appName("pyspark-notebook")\
        .master("spark://spark-master:7077")\
        .config("spark.executor.memory", "4g")\
        .config("hive.metastore.uris", "thrift://hive-metastore:9083")\
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse")\
        .enableHiveSupport()\
        .getOrCreate()
        
        url = "https://www.aemet.es/es/eltiempo/observacion/ultimosdatos_C447A_datos-horarios.xls?k=coo&l=C447A&datos=det&w=0&f=temperatura&x="
        r = requests.get(url)
        datos = pd.read_excel(r.content, skiprows=3)
        
        # Check for NaN values in the data
        if datos.isna().values.any():
            print(f"There are NaN values in the data!")
            datos = datos.replace(np.nan, 0, regex=True)
            

        
        datos_procesados = datos.rename(columns={"Fecha y hora oficial": 'Fecha', "Temperatura (ºC)" : 'Temperatura_c',
                                "Velocidad del viento (km/h)": 'Velocidad_del_viento_km_h', "Dirección del viento": 'Direccion_del_viento',
                                "Racha (km/h)": 'Racha_km_h', "Dirección de racha":'Direccion_de_racha',
                                "Precipitación (mm)": 'Precipitacion_mm', "Presión (hPa)":'Presion_hPa',
                                "Tendencia (hPa)": 'Tendencia_hPa', "Humedad (%)": 'Humedad_percent'})
        
        datos_procesados['Tendencia_hPa'].fillna(0, inplace=True)
        datos_procesados['Temperatura_c'].fillna(0, inplace=True)
        datos_procesados['Velocidad_del_viento_km_h'].fillna(0, inplace=True)
        datos_procesados['Racha_km_h'].fillna(0, inplace=True)
        datos_procesados['Precipitacion_mm'].fillna(0, inplace=True)
        datos_procesados['Presion_hPa'].fillna(0, inplace=True)
        datos_procesados['Humedad_percent'].fillna(0, inplace=True)

        
        for index, row in datos_procesados.iterrows():
            fecha_no_f = row['Fecha']
            try:
                fecha_objeto = datetime.strptime(fecha_no_f, '%Y-%m-%d %H:%M:%S')
                datos_procesados.iloc[index, datos_procesados.columns.get_loc('Fecha')] = fecha_objeto.strftime('%d/%m/%Y %H:%M')
            except ValueError:
                print(f'La fecha {fecha_no_f} no tiene el formato correcto')
        
        if not datos_procesados.empty:
            spark_df = (spark.createDataFrame(datos_procesados))
            spark.sql("use open_weather_datadb")
            spark_df.write.mode('append').saveAsTable('weather')
        else:
            print(f"Esta vacio")
        
        
    process_data()
        
        
weather_dag =  weather_etl()
    