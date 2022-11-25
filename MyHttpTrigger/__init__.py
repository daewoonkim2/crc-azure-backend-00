import logging
import azure.functions as func
from azure.core.exceptions import ResourceNotFoundError
import os
import json

from azure.data.tables import TableServiceClient, UpdateMode
connectionstring = os.environ["COSMOS_CONNECTION_STRING"]
tablename = os.environ["COSMOS_TABLE_NAME"]

table_service_client = TableServiceClient.from_connection_string(conn_str=connectionstring,table_name=tablename)
table_client = table_service_client.create_table_if_not_exists(tablename)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        res = table_client.get_entity(partition_key="visitors", row_key="count")
        res['number'] = res['number'] + 1
        visitorCount = res['number']
        table_client.upsert_entity(res, mode=UpdateMode.REPLACE)
        return func.HttpResponse(
            json.dumps({"visitors": visitorCount}),
            status_code=200
        )
    except ResourceNotFoundError:
        table_client.create_entity({"PartitionKey":"visitors", "RowKey":"count", "number":1})
        return func.HttpResponse(
            json.dumps({"visitors": 1}),
            status_code=200
        )
    except:
        return func.HttpResponse(
            status_code=400
        )

