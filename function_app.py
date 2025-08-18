import azure.functions as func
import logging

app = func.FunctionApp()

@app.cosmos_db_trigger(arg_name="azcosmosdb", container_name="adnoc-gpt",
                        database_name="agents", connection="azuren8ntutorial_DOCUMENTDB")  
def cosmosdb_trigger(azcosmosdb: func.DocumentList):
    logging.info('Python CosmosDB triggered.')
