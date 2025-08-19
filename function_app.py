import azure.functions as func
import logging

app = func.FunctionApp()

@app.cosmos_db_trigger(arg_name="azcosmosdb", 
                        container_name="agents",
                        database_name="adnoc-gpt",
                        connection="azuren8ntutorial_DOCUMENTDB",
                        lease_container_name="leases",
                        create_lease_container_if_not_exists=True)
def cosmosdb_trigger(azcosmosdb: func.DocumentList):
    logging.info('Python CosmosDB triggered.')
