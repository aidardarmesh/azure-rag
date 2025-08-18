require('dotenv').config();
const { CosmosClient } = require("@azure/cosmos");

// CosmosDB configuration from .env
const endpoint = process.env.COSMOS_ENDPOINT;
const key = process.env.COSMOS_KEY;
const databaseId = process.env.COSMOS_DATABASE_ID;
const containerId = process.env.COSMOS_CONTAINER_ID;

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

// Store seen status IDs
const seenStatusIds = new Set();

// Simple polling loop example, polling every 2 seconds
async function startPolling(sessionId) {
    console.log(`Starting polling for session_id: ${sessionId}`);

    setInterval(async () => {
        const statuses = await fetchStatusesBySessionId(sessionId);
        statuses.forEach((status) => {
            // Use status.id as unique identifier (adjust if your schema differs)
            if (!seenStatusIds.has(status.id)) {
                seenStatusIds.add(status.id);
                console.log("New status:", status.agent_name);
            }
        });
    }, 300);
}

// Replace 'your-session-id' with actual session_id you want to monitor
const sessionIdToMonitor = process.env.SESSION_ID_TO_MONITOR;

startPolling(sessionIdToMonitor);
