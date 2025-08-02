// frontend/src/services/campaignApi.js
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const apiClient = axios.create({
  baseURL: API_URL,
});

// --- Campaign Endpoints ---
export const getCampaigns = () => apiClient.get('/campaigns/');
export const createCampaign = (campaignData) => apiClient.post('/campaigns/', campaignData);
export const getCampaignById = (id) => apiClient.get(`/campaigns/${id}`);
export const startCampaign = (id) => apiClient.post(`/campaigns/${id}/start`);
export const stopCampaign = (id) => apiClient.post(`/campaigns/${id}/stop`);

// --- Contact Endpoints ---
export const addContactsToCampaign = (campaignId, file) => {
  const formData = new FormData();
  formData.append('file', file);

  return apiClient.post(`/campaigns/${campaignId}/contacts`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};