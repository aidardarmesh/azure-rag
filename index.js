const { CosmosClient } = require("@azure/cosmos");

// CosmosDB configuration
const endpoint = "https://azure-n8n-tutorial.documents.azure.com:443/";
const key = "session_id";
const databaseId = "azure-n8n-tutorial";
const containerId = "agents";

// Initialize Cosmos client and container reference
const client = new CosmosClient({ endpoint, key });
const container = client.database(databaseId).container(containerId);

// Function to fetch statuses by session_id in real-time using polling
async function fetchStatusesBySessionId(sessionId) {
  const querySpec = {
    query: "SELECT * FROM c WHERE c.session_id = @session_id",
    parameters: [{ name: "@session_id", value: sessionId }],
  };

  try {
    const { resources: items } = await container.items
      .query(querySpec, { partitionKey: sessionId })
      .fetchAll();
    return items;
  } catch (error) {
    console.error("Error fetching statuses:", error);
    return [];
  }
}

// Simple polling loop example, polling every 2 seconds
async function startPolling(sessionId) {
  console.log(`Starting polling for session_id: ${sessionId}`);

  setInterval(async () => {
    const statuses = await fetchStatusesBySessionId(sessionId);
    console.log(`Fetched ${statuses.length} statuses for session ${sessionId}:`);
    statuses.forEach((status) => console.log(status));
  }, 1000);
}

// Replace 'your-session-id' with actual session_id you want to monitor
const sessionIdToMonitor = "798e1965-9fcd-40e2-b816-b95fd27ce995";

startPolling(sessionIdToMonitor);
