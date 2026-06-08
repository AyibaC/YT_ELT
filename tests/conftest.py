import os
import pytest 
import psycopg2
from unittest import mock # use mock variables for unit tests
from airflow.models import Variable, Connection, DagBag

#first two tests check whether the variables are stored correctly 
@pytest.fixture # a fixture is a reusable piece of code used to supply input to other tests
def api_key():
    with mock.patch.dict("os.environ",AIRFLOW_VAR_API_KEY="MOCK_KEY1234"): #temporarily updates the dictionary os.environ with the key value pair provided
        yield Variable.get("API_KEY") # fetches the value of the provided airflow variable

@pytest.fixture 
def channel_handle():
    with mock.patch.dict("os.environ",AIRFLOW_VAR_CHANNEL_HANDLE="MrBeast"): #temporarily updates the dictionary os.environ with the key value pair provided
        yield Variable.get("CHANNEL_HANDLE") # fetches the value of the provided airflow variable
        
# Testing the database connection
@pytest.fixture
def mock_postgres_conn_vars():
    conn = Connection(
        login="mock_username",
        password="mock_password",
        host="mock_host",
        port=1234,
        schema="mock_db_name"
    )
    conn_url=conn.get_uri()

    with mock.patch.dict("os.environ", AIRFLOW_CONN_POSTGRES_DB_YT_ELT=conn_url):
        yield Connection.get_connection_from_secrets(conn_id="POSTGRES_DB_YT_ELT")

# testing DAGs are structured as expected
@pytest.fixture
def dagbag():
    yield DagBag()

# integration test for variables (since we are using real credentials and not mock credentials)
# get_airflow_variable is a helper function which needs to be wrapped in another to be used as a fixture
@pytest.fixture()
def airflow_variable():
    def get_airflow_variable(variable_name):
        env_var = f"AIRFLOW_VAR_{variable_name.upper()}"
        return os.getenv(env_var)
    return get_airflow_variable

# integration for connection to postgres db using real credentials
@pytest.fixture
def real_postgres_connection():
    dbname = os.getenv("ELT_DATABASE_NAME")
    user = os.getenv("ELT_DATABASE_USERNAME")
    password = os.getenv("ELT_DATABASE_PASSWORD")
    host = os.getenv("POSTGRES_CONN_HOST")
    port = os.getenv("POSTGRES_CONN_PORT")

    conn = None

    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

        yield conn

    except psycopg2.Error as e:
        pytest.fail(f"Failed to connect to database: {e}")

    finally:
        if conn:
            conn.close()