import unittest
from unittest.mock import patch, Mock
from azure.core.exceptions import ResourceNotFoundError
import azure.functions as func
import json

azure_mock = Mock()

class tests (unittest.TestCase):

    #response should return 1, status code 200
    @patch("os.environ", {"COSMOS_CONNECTION_STRING":"test_conn.db", "COSMOS_TABLE_NAME":"test_table", "COSMOS_DB_NAME": "test_db_name"})
    @patch("azure.data.tables.TableServiceClient", azure_mock)
    def test_first_visit (self):
        azure_mock.from_connection_string.return_value.create_table_if_not_exists.return_value.get_entity.side_effect = ResourceNotFoundError()

        import function_app

        req = func.HttpRequest(
            method = 'GET',
            body = None,
            url = '/api/visit'
        )

        func_call = function_app.main.build().get_user_function()

        resp:func.HttpResponse = func_call(req)

        self.assertEqual(json.loads(resp.get_body())['visitors'], 1)
        self.assertEqual(resp.status_code, 200)
        azure_mock.from_connection_string.return_value.create_table_if_not_exists.return_value.get_entity.reset_mock(side_effect=True)
        azure_mock.reset_mock()

    @patch("os.environ", {"COSMOS_CONNECTION_STRING":"test_conn.db", "COSMOS_TABLE_NAME":"test_table", "COSMOS_DB_NAME": "test_db_name"})
    @patch("azure.data.tables.TableServiceClient", azure_mock)
    def test_visit (self):
        base = 10
        azure_mock.from_connection_string.return_value.create_table_if_not_exists.return_value.get_entity.return_value = {"number":base}

        import function_app

        req = func.HttpRequest(
            method = 'GET',
            body = None,
            url = '/api/visit'
        )

        func_call = function_app.main.build().get_user_function()

        resp:func.HttpResponse = func_call(req)

        #db read is called
        azure_mock.from_connection_string.return_value.create_table_if_not_exists.return_value.get_entity.assert_called_once()

        #update_visitor_count is called
        azure_mock.from_connection_string.return_value.create_table_if_not_exists.return_value.upsert_entity.assert_called_once()

        #visitor value return should be visitor value+1 / should be increased
        self.assertEqual(json.loads(resp.get_body())['visitors'], base+1)
        self.assertEqual(resp.status_code, 200)
        azure_mock.reset_mock()

    #general error response should return 1, status 400
    @patch("os.environ", {"COSMOS_CONNECTION_STRING":"test_conn.db", "COSMOS_TABLE_NAME":"test_table", "COSMOS_DB_NAME": "test_db_name"})
    @patch("azure.data.tables.TableServiceClient", azure_mock)
    def test_error (self):
        import function_app

        req = func.HttpRequest(
            method = 'GET',
            body = None,
            url = '/api/visit'
        )

        func_call = function_app.main.build().get_user_function()

        resp:func.HttpResponse = func_call(req)
        self.assertEqual(json.loads(resp.get_body())['visitors'], 0)
        self.assertEqual(resp.status_code, 400)
        azure_mock.reset_mock()

if __name__ == '__main__':
    unittest.main()