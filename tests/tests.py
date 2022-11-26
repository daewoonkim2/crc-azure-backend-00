import unittest

import azure.functions as func

from function_app import main

#asks for visitor
#increases the visitor count
#returns the visitor count increased by 1

#what if db is down

class tests (unittest.TestCase):
    async def test_increase (self):
        req = func.HttpRequest(method="GET",
        body = None,
        url = '/',
        params = {})

        resp = await main(req)

        self.assertEquals(resp.get_body(), )

    async def test_db_down (self):
        self.assertEquals()


