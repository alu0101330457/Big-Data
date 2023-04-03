from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'Mario',
    'retries': 5,
    'retry_delay' : timedelta(minutes=5)
}


def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f"Im {first_name} {last_name}, and Im {age} years old.")

def get_name(ti):
    ti.xcom_push(key= 'first_name', value='Mario')
    ti.xcom_push(key= 'last_name', value='Clavijo')
    
def get_age(ti):
    ti.xcom_push(key = 'age', value = '22')

with DAG(
    dag_id='dag_python_operator_v5',
    default_args=default_args,
    description='This is the first dag I wrote that will run python operators',
    start_date=datetime.now(),
    schedule_interval='@daily'
    
) as dag:
    
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet
        # op_kwargs={'age': 21}
    )

    task2 = PythonOperator(
        task_id = 'get_name',
        python_callable = get_name
    )
    
    task3 = PythonOperator(
        task_id = 'get_age',
        python_callable= get_age
    )
    
      
    [task2, task3] >> task1