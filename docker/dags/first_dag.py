
from datetime import datetime, timedelta

from airflow import DAG

from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Mario',
    'retries': 5,
    'retry_delay' : timedelta(minutes=2)
}

with DAG(
    dag_id='First_dag_v5',
    default_args=default_args,
    description='This is the first dag I wrote',
    start_date=datetime.now(),
    schedule_interval='@daily'
    
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command="echo Hello Mario, this is your first task on Airflow!!!"
    )
    
    task2 = BashOperator(
        task_id='second_task',
        bash_command="echo Im the second task and the first task executed first"
    )
    
    task3 = BashOperator(
        task_id='third_task',
        bash_command="echo Im the third task and ill execute with the task2"
    )
    
    #task dependency method 1
    #task1.set_downstream(task2)
    #task1.set_downstream(task3)
    
    #task dependency method 2
    #task1 >> task2
    #task1 >> task3
    
    #task dependency method 3
    
    task1 >> [task2, task3]