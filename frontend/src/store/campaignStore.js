// frontend/src/store/campaignStore.js
import { create } from 'zustand';
import * as campaignApi from '../services/campaignApi';

const useCampaignStore = create((set) => ({
  campaigns: [],
  currentCampaign: null,
  loading: false,
  error: null,
  
  fetchCampaigns: async () => {
    set({ loading: true, error: null });
    try {
      const response = await campaignApi.getCampaigns();
      set({ campaigns: response.data, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  fetchCampaignById: async (id) => {
    set({ loading: true, error: null, currentCampaign: null });
    try {
      const response = await campaignApi.getCampaignById(id);
      set({ currentCampaign: response.data, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  createCampaign: async (campaignData) => {
    set({ loading: true, error: null });
    try {
      await campaignApi.createCampaign(campaignData);
      // After creating, refetch the list to show the new campaign
      const response = await campaignApi.getCampaigns();
      set({ campaigns: response.data, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  // Add more actions for start/stop/addContacts later
}));

export default useCampaignStore;