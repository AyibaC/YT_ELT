def test_api_key(api_key): # test functions must stary with test_. since we used api_key as the parameter, pytest knows to pick up the fixture api_key from the conftest file
    assert api_key == "MOCK_KEY1234" # checking that we get the value we expect from the function we defined in conftest.py


def test_channel_handle(channel_handle):
    assert channel_handle == "MrBeast"

def test_postgres_conn(mock_postgres_conn_vars):
    conn = mock_postgres_conn_vars
    assert conn.login == "mock_username"
    assert conn.password == "mock_password"
    assert conn.host == "mock_host"
    assert conn.port == 1234
    assert conn.schema == "mock_db_name"


def test_dags_integrity(dagbag):
    # check there are no import errors
    assert dagbag.import_errors == {}, f"Import errorrs found: {dagbag.import_errors}"
    print("==================")
    print(dagbag.import_errors)


    # check that all dags are being loaded
    expected_dag_ids = ["produce_json","update_db", "data_quality"]
    loaded_dag_ids = list(dagbag.dags.keys())
    print("==================")
    print(dagbag.dags.keys())

    for dag_id in expected_dag_ids:
        assert dag_id in loaded_dag_ids, f"DAG {dag_id} is missing"


    # check that there are the correct number of dags
    assert dagbag.size() == 3
    print("==================")
    print(dagbag.size())


    # check that each dag has the right number of tasks
    expected_task_counts = {
        "produce_json": 4,
        "update_db": 2,
        "data_quality": 2
    }
    print("==================")
    for dag_id, dag in dagbag.dags.items():
        expected_count=expected_task_counts[dag_id]
        actual_count = len(dag.tasks)
        assert(
            expected_count == actual_count
        ), f"DAG {dag_id} has actual count {actual_count} and expected count{expected_count}"
        print(dag_id, len(dag.tasks))