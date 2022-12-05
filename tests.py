import unittest
from unittest.mock import patch, Mock, MagicMock, ANY
mock_table_service_client = MagicMock()

from azure.core.exceptions import ResourceNotFoundError

import azure.functions as func

import json

class tests (unittest.TestCase):

    #response should return 1, status code 200
    @patch("os.environ", {"COSMOS_CONNECTION_STRING":"test_conn.db", "COSMOS_TABLE_NAME":"test_table", "COSMOS_DB_NAME": "test_db_name"})
    @patch("azure.data.tables.TableServiceClient.from_connection_string", mock_table_service_client)
    # @patch("TableServiceClient.create_table_if_not_exists", mock_table_client)
    def test_first_visit (self):
        mock_table_client = MagicMock(get_entity = {'visitors': '1'})
        mock_table_service_client (create_table_if_not_exists=mock_table_client)
        from function_app import main

        req = func.HttpRequest(
            method = 'GET',
            body = None,
            url = '/api/visit'
        )

        func_call = main.build().get_user_function()

        resp:func.HttpResponse = func_call(req)

        self.assertEqual(json.loads(resp.get_body())['visitors'], 1)
        self.assertEqual(resp.status_code, 200)
        
        # mock_table_service_client.from_connection_string.assert_called_once()
        # mock_table_service_client.get_entity.assert_called_once()
        mock_table_service_client.reset_mock()

    @patch("azure.data.tables.TableServiceClient.from_connection_string", mock_table_service_client)
    def test_visit (self):
        #db read is called
        #mock_table_service_client.get_entity.assert_called_once()
        # mock_table_service_client.get_entity
        # mock_table_service_client.assert_called

        #update_visitor_count is called
        #mock_table_service_client .upsert_entity.assert_called_once()

        #get visitor value

        #second call
        #return should be visitor value+1 / should be increased
        mock_table_service_client.reset_mock()


    #general error response should return 1, status 400
    @patch("os.environ", {"COSMOS_CONNECTION_STRING":"test_conn.db", "COSMOS_TABLE_NAME":"test_table", "COSMOS_DB_NAME": "test_db_name"})
    @patch("azure.data.tables.TableServiceClient", mock_table_service_client)
    def test_error (self):
        from function_app import main

        req = func.HttpRequest(
            method = 'GET',
            body = None,
            url = '/api/visit'
        )

        func_call = main.build().get_user_function()
        resp:func.HttpResponse = func_call(req)
        self.assertEqual(json.loads(resp.get_body())['visitors'], 0)
        self.assertEqual(resp.status_code, 400)
        mock_table_service_client.reset_mock()

if __name__ == '__main__':
    unittest.main()
