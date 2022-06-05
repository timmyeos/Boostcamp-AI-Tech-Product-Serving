from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {    # 항상 DAG 만들 때 주입시켜주는 인자
    'owner': 'kyle',
    'depends_on_past': False,  # 이전 DAG의 Task가 성공, 실패 여부에 따라 현재 DAG 실행 여부가 결정. False는 과거의 실행 결과 상관없이 매일 실행한다
    'start_date': datetime(2022, 4, 20),
    'retires': 1,  # 실패시 재시도 횟수
    'retry_delay': timedelta(minutes=5)  # 만약 실패하면 5분 뒤 재실행
    # 'priority_weight': 10 # DAG의 우선 순위를 설정할 수 있음
    # 'end_date': datetime(2022, 4, 24) # DAG을 마지막으로 실행할 Date
    # 'execution_timeout': timedelta(seconds=300), # 실행 타임아웃 : 300초 넘게 실행되면 종료
    # 'on_failure_callback': some_function # 만약에 Task들이 실패하면 실행할 함수
    # 'on_success_callback': some_other_function
    # 'on_retry_callback': another_function
}

# with 구문으로 DAG 정의
with DAG(
        dag_id='bash_dag',
        default_args=default_args,
        schedule_interval='@once',  # DAG을 어떤 주기로 실행, 크론표현식
        tags=['my_dags']
) as dag:
    # BashOperator 사용
    task1 = BashOperator(
        task_id='print_date',  # task의 id
        bash_command='date'  # 실행할 bash command
    )

    task2 = BashOperator(
        task_id='sleep',
        bash_command='sleep 5', # 5초 동안 쉬겠다
        retries=2  # 만약 bash command가 실패하면 2번 재시도한다
    )

    task3 = BashOperator(
        task_id='pwd',
        bash_command='pwd'
    )

    task1 >> task2  # task1 이후에 task2 실행
    task1 >> task3  # task1 이후에 task3 실행(2와 3을 병렬로 실행)
    ### db 부하 덜 주려고 스케쥴러는 5분마다 스캔
    ### 재실행하고 싶으면 DAG run의 clear 누르면 그 시간에 실행하기로 했던 작업들 다시 실행됨
    