import logging
import azure.functions as func
from azure.core.exceptions import ResourceNotFoundError
import os
import json

from azure.data.tables import TableServiceClient, UpdateMode, TableEntity

connectionstring = os.environ["COSMOS_CONNECTION_STRING"]
tablename = os.environ["COSMOS_TABLE_NAME"]
dbname = os.environ["COSMOS_DB_NAME"]

table_service_client = TableServiceClient.from_connection_string(conn_str=connectionstring,table_name=tablename)
table_client = table_service_client.create_table_if_not_exists(tablename)

app = func.FunctionApp()

@app.function_name(name="CosmosDBTrigger1")
@app.cosmos_db_trigger(arg_name="documents", database_name=dbname, collection_name=tablename, connection_string_setting=connectionstring,
 lease_collection_name="leases", create_lease_collection_if_not_exists="true")
def db_trigger_test (documents: func.DocumentList):
    if documents:
        logging.info('Document id: %s', documents[0]['id'])

def update_visitor_count (res: TableEntity):
    try:
        logging.info('updating database')
        res['number'] = res['number'] + 1
        table_client.upsert_entity(res, mode=UpdateMode.REPLACE)
        logging.info('updated database')
    except Exception:
        logging.critical('ran into problem updating visitor count')

@app.function_name (name="HttpTrigger1")
@app.route("visit")
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        res = table_client.get_entity(partition_key="visitors", row_key="count")
        num_of_visitors = res['number']
        logging.info('read database')
        update_visitor_count(res)
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
        logging.critical()
        return func.HttpResponse(
            json.dumps({"visitors": 1}),
            status_code=400
        )

