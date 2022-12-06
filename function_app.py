import logging
import azure.functions as func
from azure.core.exceptions import ResourceNotFoundError
import os
import json

from azure.data.tables import TableServiceClient, TableClient, UpdateMode, TableEntity

app = func.FunctionApp()

connectionstring = os.environ["COSMOS_CONNECTION_STRING"]
tablename = os.environ["COSMOS_TABLE_NAME"]
dbname = os.environ["COSMOS_DB_NAME"]

def read_visitor_count (res: TableClient):
    logging.info('reading database')
    return res.get_entity(partition_key="visitors", row_key="count")

def update_visitor_count (table_client: TableClient, table_entity: TableEntity):
    logging.info('updating database')
    table_entity['number'] = table_entity['number'] + 1
    table_client.upsert_entity(table_entity, mode=UpdateMode.REPLACE)

@app.function_name (name="HttpTrigger1")
@app.route("visit")
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    table_service_client = TableServiceClient.from_connection_string(conn_str=connectionstring,table_name=tablename)
    table_client = table_service_client.create_table_if_not_exists(tablename)

    try:
        res = read_visitor_count(table_client)
        num_of_visitors = res['number']
        logging.info('read database')
        
        update_visitor_count(table_client, res)
        logging.info('updated database')
        return func.HttpResponse(
            json.dumps({"visitors": num_of_visitors+1}),
            status_code=200
        )
    except ResourceNotFoundError:
        logging.warn('entity is missing, attempting to initialize table')
        table_client.create_entity({"PartitionKey":"visitors", "RowKey":"count", "number":1})
        return func.HttpResponse(
            json.dumps({"visitors": 1}),
            status_code=200
        )
    except Exception as e:
        logging.critical(e)
        return func.HttpResponse(
            json.dumps({"visitors": 0}),
            status_code=400
        )

