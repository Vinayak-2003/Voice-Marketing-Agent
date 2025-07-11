// frontend/src/store/agentStore.js
import { create } from 'zustand';
import * as agentApi from '../services/agentApi';

const useAgentStore = create((set) => ({
  agents: [],
  currentAgent: null,
  loading: false,
  error: null,

  fetchAgents: async () => {
    set({ loading: true, error: null });
    try {
      const response = await agentApi.getAgents();
      set({ agents: response.data, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  fetchAgentById: async (id) => {
    set({ loading: true, error: null });
    try {
      const response = await agentApi.getAgentById(id);
      set({ currentAgent: response.data, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  createAgent: async (agentData) => {
    set({ loading: true, error: null });
    try {
      const response = await agentApi.createAgent(agentData);
      set((state) => ({
        agents: [...state.agents, response.data],
        loading: false,
      }));
    } catch (error) {
      set({ error: error.message, loading: false });
      throw error; // Re-throw to be caught in the component
    }
  },
}));

export default useAgentStore;