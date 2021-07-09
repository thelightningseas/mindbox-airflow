from datetime import timedelta, datetime
import uuid

from airflow import DAG

from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount


def get_tenants_to_recalculate():
    # will be replaced with a caprica API call in production
    return [
        {
            "serverHostName": "db-baon.corp.itcd.ru",
            "databaseName": "baon",
            "executionId": str(uuid.uuid4())
        },
        {
            "serverHostName": "db-bethowen.corp.itcd.ru",
            "databaseName": "bethowen",
            "executionId": str(uuid.uuid4())
        },
        {
            "serverHostName": "db-vamsvet.corp.itcd.ru",
            "databaseName": "vamsvet",
            "executionId": str(uuid.uuid4())
        }
    ]


dag = DAG(
    'optimal_sending_time',
    default_args={
        'owner': 'Mindbox',
        'depends_on_past': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='Optimal sending time algorithm recalculation for all tenants',
    schedule_interval=timedelta(days=1),
    start_date=datetime(1970, 1, 1),
    tags=['non-gpu']
)

for tenant_params in get_tenants_to_recalculate():
    DockerOperator(
        task_id=tenant_params["databaseName"],
        environment=tenant_params,
        mounts=[
            Mount(target="/opt/assets", source="assets", read_only=True, type="volume"),
            Mount(target="/opt/results", source="results", read_only=False, type="volume"),
        ],
        image="optimal_sending_time",
        force_pull=False,
        user="root",
        privileged=True,
        auto_remove=True,
        dag=dag
    )
