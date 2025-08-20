import azure.functions as func
import logging
from pprint import pprint

app = func.FunctionApp()

@app.cosmos_db_trigger(arg_name="azcosmosdb", 
                        container_name="agents",
                        database_name="adnoc-gpt",
                        connection="azuren8ntutorial_DOCUMENTDB",
                        lease_container_name="leases",
                        create_lease_container_if_not_exists=True)
def cosmosdb_trigger(azcosmosdb: func.DocumentList):
    if azcosmosdb:
        logging.info("Changes detected in CosmosDB 'agents' container.")
        for doc in azcosmosdb:
            # Log the full document received by the trigger
            logging.info(f"Document received: {doc.to_json()}")
    else:
        logging.info("No documents received from the trigger.")
