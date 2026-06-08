from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.video_stats import get_playlist_id, get_video_ids, extract_video_data, save_to_json
from datawarehouse.dwh import staging_table, core_table

local_tz = pendulum.timezone("Europe/London")

default_args = {
    "owner": "dataengineers",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "ayibacesario@hotmail.co.uk",
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2026, 1, 1, tzinfo=local_tz) # starts at the end of the first interval after startdate (e.g. end of the next day for daily runs)
}

with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description='DAG to produce json file of the raw data',
    schedule='0 14 * * *',
    catchup=False
) as dag:
    # Define tasks 
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extract_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(extract_data)

    # Define dependencies
    playlist_id >> video_ids >> extract_data >> save_to_json_task


with DAG(
    dag_id='update_db',
    default_args=default_args,
    description='DAG to process json file and insert data into staging and core schemas',
    schedule='0 15 * * *',
    catchup=False
) as dag:
    # Define tasks 
    update_staging = staging_table()
    update_core = core_table()

    # Define dependencies
    update_staging >> update_core 