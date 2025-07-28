// frontend/src/services/callApi.js
import axios from 'axios';

// Ensure the base URL does NOT have a trailing slash
const API_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const apiClient = axios.create({
  baseURL: API_URL,
});

export const originateCall = (toNumber, agentId) => {
  // This function creates the JSON payload.
  // The keys 'to_number' and 'agent_id' must match the Pydantic model exactly.
  return apiClient.post('/calls/originate', {
    to_number: toNumber,
    agent_id: agentId,
  });
};