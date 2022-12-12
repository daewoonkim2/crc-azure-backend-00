import unittest
from unittest.mock import patch, Mock, MagicMock

from azure.core.exceptions import ResourceNotFoundError

import azure.functions as func

import json

import function_app
function_app.os.environ = {"COSMOS_CONNECTION_STRING":"test_conn.db", "COSMOS_TABLE_NAME":"test_table", "COSMOS_DB_NAME": "test_db_name"}

class tests (unittest.TestCase):

    #response should return 1, status code 200
    @patch("os.environ", {"COSMOS_CONNECTION_STRING":"test_conn.db", "COSMOS_TABLE_NAME":"test_table", "COSMOS_DB_NAME": "test_db_name"})
    def test_first_visit (self):
        self.assertEqual("", "")

    def test_visit (self):
        #db read is called

        #update_visitor_count is called

        #get visitor value

        #second call
        #return should be visitor value+1 / should be increased
        self.assertEqual("", "")

    #general error response should return 1, status 400
    def test_error (self):
        req = func.HttpRequest(
            method = 'GET',
            body = None,
            url = '/api/visit'
        )

        func_call = function_app.main.build().get_user_function()
        resp:func.HttpResponse = func_call(req)
        self.assertEqual(json.loads(resp.get_body())['visitors'], 0)
        self.assertEqual(resp.status_code, 400)

if __name__ == '__main__':
    unittest.main()