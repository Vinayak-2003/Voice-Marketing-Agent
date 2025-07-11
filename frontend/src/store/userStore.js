// frontend/src/store/userStore.js
import { create } from 'zustand';

const useUserStore = create((set) => ({
  user: null, // e.g., { name: 'Admin', role: 'admin' }
  isAuthenticated: false,
  
  login: (userData) => set({ user: userData, isAuthenticated: true }),
  logout: () => set({ user: null, isAuthenticated: false }),
}));

export default useUserStore;