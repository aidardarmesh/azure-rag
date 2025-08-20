import azure.functions as func
from azure.functions import SignalRMessage
import logging

app = func.FunctionApp()

@app.cosmos_db_trigger(
    arg_name="azcosmosdb",
    container_name="agents",
    database_name="adnoc-gpt",
    connection="azuren8ntutorial_DOCUMENTDB",
    lease_container_name="leases",
    create_lease_container_if_not_exists=True)
@app.signalr_output(
    arg_name="signalr_messages",
    hub_name="agentsHub",
    connection="AzureSignalRConnectionString"
)
def cosmosdb_trigger(
    azcosmosdb: func.DocumentList,
    signalr_messages: func.Out[func.SignalRMessage]
):
    if azcosmosdb:
        logging.info(f"{len(azcosmosdb)} document changes detected.")
        messages = []
        for doc in azcosmosdb:
            # Send each changed document as a SignalR message to all clients
            message = SignalRMessage(
                target="newAgentUpdate",
                arguments=[doc.to_json()]
            )
            messages.append(message)

        signalr_messages.set(messages)
    else:
        logging.info("No document changes detected.")

# HTTP triggered function to provide SignalR connection info to frontend
@app.function_name(name="negotiate")
@app.route(route="negotiate", methods=["GET"])
@app.signalr_connection_info(
    name="signalRConnectionInfo",
    hub_name="agentsHub",
    connection_string_setting="AzureSignalRConnectionString"
)
def negotiate(req: func.HttpRequest, 
              signalRConnectionInfo: func.Out[func.SignalRConnectionInfo]) -> func.HttpResponse:
    return func.HttpResponse(signalRConnectionInfo.get(), status_code=200, mimetype="application/json")
