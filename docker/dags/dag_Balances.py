from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.hive_operator import HiveOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from datetime import datetime, timedelta
from pyhive import hive
import requests
import pandas as pd
import numpy as np
import io




def fetch_information_2018_2019():
    
    #Here we get the balance sheets from the URL and then we turn into excel file.
    response = requests.get("https://www.unacc.com/wp-content/uploads/2020/03/Balances.xlsx", verify=False)
    excel_file = pd.ExcelFile(response.content)
    
    #here we get the sheet names from the excel file that contains the word 'Individual' and this  search start from 
    #the sheet number 13.
    sheet_names = [sheet_name for sheet_name in excel_file.sheet_names[13:] if "Individual" in sheet_name]
    
    #this piece of code create a list of DataFrames, one for each sheet in the excel file that contains 
    #the word 'Individual'
    dfs = [
    pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=4)
    for sheet_name in sheet_names]
    
    return dfs
    
    
def fetch_information_2020():
    #Here we get the balance sheets from the URL and then we turn into excel file.
    response = requests.get("https://www.unacc.com/wp-content/uploads/2021/03/Balances-2020.xlsx", verify=False)
    excel_file = pd.ExcelFile(response.content)
    
    #here we get the sheet names from the excel file that contains the word 'Individual' and this  search start from 
    #the sheet number 1.
    sheet_names = [sheet_name for sheet_name in excel_file.sheet_names[1:] if "Individual" in sheet_name]
    
    #this piece of code create a list of DataFrames, one for each sheet in the excel file that contains 
    #the word 'Individual'
    dfs = [
    pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=4)
    for sheet_name in sheet_names]
    
    return dfs
    

def fetch_information_2021():
    #Here we get the balance sheets from the URL and then we turn into excel file.
    response = requests.get("https://www.unacc.com/wp-content/uploads/2022/05/Balances-2021.xlsx", verify=False)
    excel_file = pd.ExcelFile(response.content)
    
    #here we get the sheet names from the excel file that contains the word 'Individual' and this  search start from 
    #the sheet number 1.
    sheet_names = [sheet_name for sheet_name in excel_file.sheet_names[1:] if "Individual" in sheet_name]
    
    #this piece of code create a list of DataFrames, one for each sheet in the excel file that contains 
    #the word 'Individual'
    dfs = [
    pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=4)
    for sheet_name in sheet_names]
    
    return dfs
    
    
def fetch_information_2022():
    #Here we get the balance sheets from the URL and then we turn into excel file.
    response = requests.get("https://www.unacc.com/wp-content/uploads/2023/03/Balances-2022.xlsx", verify=False)
    excel_file = pd.ExcelFile(response.content)
    
    #here we get the sheet names from the excel file that contains the word 'Individual' and this  search start from 
    #the sheet number 1.
    sheet_names = [sheet_name for sheet_name in excel_file.sheet_names[1:] if "Individual" in sheet_name]
    
    #this piece of code create a list of DataFrames, one for each sheet in the excel file that contains 
    #the word 'Individual'
    dfs = [
    pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=4)
    for sheet_name in sheet_names]
    
    return dfs
    
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    
    # Clean blanks
    df = df.dropna(how="all", axis="rows")
    df = df.dropna(how="all", axis="columns")
    df = df.rename(columns={df.columns[0]: "EPIGRAFE"})
    if 'Unnamed: 6' in df.columns:
        df = df.drop(columns=['Unnamed: 6'])
        
    df = df.dropna(subset=['EPIGRAFE'])

    # Clean date
    fecha_datos = df.iloc[0, -1]
    df = df.iloc[1:]
    df = df.reset_index(drop=True)

    # Orden epigrafe
    df["ORDEN_EPIGRAFE"] = df.index

    # Unpivot
    df = pd.melt(df, id_vars=["EPIGRAFE", "ORDEN_EPIGRAFE"], var_name="ENTIDAD", value_name="VALOR")
    df["FECHA"] = fecha_datos
    
    # Nan values 
    df['VALOR'].fillna(0, inplace=True)

    return df


def cleaning_process(dfs):
    clean_dfs = [clean_dataframe(df) for df in dfs]
    df = pd.concat(clean_dfs)

    df["NIVEL_EPIGRAFE"] = df.EPIGRAFE.str.len() - df.EPIGRAFE.str.lstrip().str.len()
    df["EPIGRAFE"] = df.EPIGRAFE.str.strip()
    df["COD_ENTIDAD"] = df.ENTIDAD.str[:5].str.strip()
    
    return df

def create_hive_table():
    conn = hive.Connection(host="host.docker.internal", port=10000, username="hive", database="Balancesdb")
    cursor = conn.cursor()

    # Creation of hive table for 2018 and 2019 data
    create_table_query_2018_2019 = """
       CREATE EXTERNAL TABLE IF NOT EXISTS balances1819 (
            epigrafe STRING,
            orden_epigrafe STRING,
            entidad STRING,
            valor STRING,
            fecha STRING,
            nivel_epigrafe STRING,
            cod_entidad STRING
            )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\n'
    """
    # Creation of hive table for 2020 data
    create_table_query_2020 = """
       CREATE EXTERNAL TABLE IF NOT EXISTS balances20 (
            epigrafe STRING,
            orden_epigrafe STRING,
            entidad STRING,
            valor STRING,
            fecha STRING,
            nivel_epigrafe STRING,
            cod_entidad STRING
            )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\n'
    """
    
    # Creation of hive table for 2021 data
    create_table_query_2021 = """
       CREATE EXTERNAL TABLE IF NOT EXISTS balances21 (
            epigrafe STRING,
            orden_epigrafe STRING,
            entidad STRING,
            valor STRING,
            fecha STRING,
            nivel_epigrafe STRING,
            cod_entidad STRING
            )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\n'
    """
    
    # Creation of hive table for 2022 data
    create_table_query_2022 = """
       CREATE EXTERNAL TABLE IF NOT EXISTS balances22 (
            epigrafe STRING,
            orden_epigrafe STRING,
            entidad STRING,
            valor STRING,
            fecha STRING,
            nivel_epigrafe STRING,
            cod_entidad STRING
            )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\n'
    """
    cursor.execute(create_table_query_2018_2019)
    cursor.execute(create_table_query_2020)
    cursor.execute(create_table_query_2021)
    cursor.execute(create_table_query_2022)
    
    # Close the connection
    conn.commit()
    cursor.close()
    conn.close()


def insert_data():
    conn = hive.Connection(host="host.docker.internal", port=10000, username="hive", database="Balancesdb")
    cursor = conn.cursor()

    balance_data_18_19 = cleaning_process(fetch_information_2018_2019())
    balances_data20 = cleaning_process(fetch_information_2020())
    balances_data21 = cleaning_process(fetch_information_2021())
    balances_data22 = cleaning_process(fetch_information_2022())
    
    insert_query = "INSERT INTO TABLE balances1819 VALUES (%s, %s, %s, %s, %s, %s, %s)"
    for row in balance_data_18_19.itertuples(index=False):
        cursor.execute(insert_query, (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    # insert_query = "INSERT INTO TABLE balances20 VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # for row in balances_data20.itertuples(index=False):
    #     cursor.execute(insert_query, (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    # insert_query = "INSERT INTO TABLE balances21 VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # for row in balances_data21.itertuples(index=False):
    #     cursor.execute(insert_query, (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        
    # insert_query = "INSERT INTO TABLE balances22 VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # for row in balances_data22.itertuples(index=False):
    #     cursor.execute(insert_query, (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    # close the connection
    conn.commit()
    cursor.close()
    conn.close()
    
default_args = {
    'owner': 'Mario',
    'start_date': datetime(2023, 4, 26),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='dag_balances_v2',
    default_args=default_args,
    description='This is a dag that fetch information about caja siete.',
    start_date=datetime(2023,4,26),
    schedule_interval='@daily'

) as dag:
    
    create_tables = PythonOperator(
    task_id='create_table',
    python_callable=create_hive_table,
    dag=dag
    )
    
    fetch_and_insert_data = PythonOperator(
    task_id='fetch_and_insert_data',
    python_callable=insert_data,
    dag=dag
    )
    
    
    create_tables >> fetch_and_insert_data
