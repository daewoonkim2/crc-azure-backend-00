import unittest
from unittest.mock import MagicMock, patch

import logging
import azure.functions as func
from azure.core.exceptions import ResourceNotFoundError
import os
import json
from azure.data.tables import TableServiceClient, UpdateMode, TableEntity


os.environ['COSMOS_CONNECTION_STRING']="test_conn.db"
os.environ['COSMOS_TABLE_NAME']="test_table"
os.environ['COSMOS_DB_NAME']="test_db_name"

#response should return 1, status code 200

@patch('function_app.TableServiceClient')
def test_first_visit (mock_tsc: MagicMock):
    import function_app
    # function_app.connectionstring="test_conn.db"
    # function_app.tablename="test_table"
    # function_app.dbname="test_db_name"
    
    ts_mock = MagicMock()
    ts_mock.get_entity.return_value = {'number':'1'}
    mock_tsc.from_connection_string.return_value = ts_mock

    req = func.HttpRequest(
        method = 'GET',
        body = None,
        url = '/api/visit'
    )

    func_call = function_app.main.build().get_user_function()
    resp:func.HttpResponse = func_call(req)

    assert json.loads(resp.get_body())['visitors'] ==  1
    assert resp.status_code == 200

    assert "" == ""

# @patch('os.environ', {"COSMOS_CONNECTION_STRING":"test_conn.db", "COSMOS_TABLE_NAME":"test_table", "COSMOS_DB_NAME": "test_db_name"})
# @patch('function_app.TableServiceClient')
# def test_visit (mock_tsc: MagicMock):
#     #db read is called

#     #update_visitor_count is called
#     #mock_table_service_client .upsert_entity.assert_called_once()

#     #get visitor value

#     #second call
#     #return should be visitor value+1 / should be increased
#     assert "" == ""

# @patch('os.environ', {"COSMOS_CONNECTION_STRING":"test_conn.db", "COSMOS_TABLE_NAME":"test_table", "COSMOS_DB_NAME": "test_db_name"})
# @patch('function_app.TableServiceClient')
# #general error response should return 1, status 400
# def test_error (mock_tsc: MagicMock):
#     from function_app import main

#     req = func.HttpRequest(
#         method = 'GET',
#         body = None,
#         url = '/api/visit'
#     )

#     func_call = main.build().get_user_function()
#     resp:func.HttpResponse = func_call(req)
#     assert json.loads(resp.get_body())['visitors'] ==  0
#     assert resp.status_code == 400
