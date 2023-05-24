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
import snscrape.modules.twitter as sntwitter



def etl_process():
    query = "cajasiete"
    tweets = []
    User = []
    limit = 50

    for tweet in sntwitter.TwitterSearchScraper(query).get_items():

        if len(tweets) == limit:
            break
        else:
            tweets.append([tweet.date, tweet.user.id , tweet.id ,tweet.rawContent, tweet.retweetCount, tweet.likeCount, tweet.lang, tweet.user.location])
            User.append([tweet.user.id, tweet.user.username, tweet.user.profileImageUrl,tweet.user.followersCount])



    dfTweet = pd.DataFrame(tweets, columns=['datetweet', 'userid', 'tweetid', 'tweet', 'retweetcount', 'likecount', 'lang', 'locationtweet'])


    return dfTweet


def create_hive_table():
    conn = hive.Connection(host="host.docker.internal", port=10000, username="hive", database="tweetsdb")
    cursor = conn.cursor()

    # Creamos una tabla en Hive
    create_table_query = """
       CREATE EXTERNAL TABLE IF NOT EXISTS tweets (
            DateTweet STRING,
            UserID STRING,
            TweetID STRING,
            Tweet STRING,
            RetweetCount STRING,
            LikeCount STRING,
            Lang STRING,
            LocationTweet STRING

            )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            LINES TERMINATED BY '\n'
    """
    cursor.execute(create_table_query)

    datos = etl_process()

    print(datos.head())
    print(datos.columns)
    print(datos.describe())
  
    insert_query = "INSERT INTO TABLE tweets VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    for row in datos.itertuples(index=False):
        cursor.execute(insert_query, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    # Cerramos la conexión
    conn.commit()
    cursor.close()
    conn.close()

    print("Tabla creada exitosamente")



default_args = {
    'owner': 'Mario',
    'start_date': datetime(2023, 4, 12),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='dag_pyhive',
    default_args=default_args,
    description='This is a dag that help us to get social media info',
    start_date=datetime(2023,4,8),
    schedule_interval='@daily'

) as dag:

    create_table_operator = PythonOperator(
    task_id='create_table',
    python_callable=create_hive_table,
    dag=dag
    )

    create_table_operator