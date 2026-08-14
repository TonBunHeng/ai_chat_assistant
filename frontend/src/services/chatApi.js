import axios from 'axios';

// Base API URL (falls back to live Render backend if env var is unset)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://ai-chatbot-pud2.onrender.com/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

/**
 * Send chat message to AI assistant
 */
export const sendMessage = async ({ message, language = 'en', session_id = null }) => {
  try {
    const response = await apiClient.post('/chat', {
      message,
      language,
      session_id,
    });
    return response.data;
  } catch (error) {
    console.error('API sendMessage error:', error);
    throw error.response?.data?.detail || error.message || 'Failed to communicate with AI Backend.';
  }
};

/**
 * Get all active chat sessions
 */
export const fetchChatSessions = async () => {
  try {
    const response = await apiClient.get('/chat/sessions');
    const res = response.data;
    if (res && res.data && Array.isArray(res.data)) {
      return res.data;
    }
    return Array.isArray(res) ? res : [];
  } catch (error) {
    console.error('API fetchChatSessions error:', error);
    return [];
  }
};

/**
 * Get message history for specific session
 */
export const fetchChatSession = async (sessionId) => {
  try {
    const response = await apiClient.get(`/chat/sessions/${sessionId}`);
    const res = response.data;
    return res && res.data ? res.data : res;
  } catch (error) {
    console.error('API fetchChatSession error:', error);
    throw error;
  }
};

/**
 * Delete / Clear specific chat session
 */
export const deleteChatSession = async (sessionId) => {
  try {
    const response = await apiClient.delete(`/chat/sessions/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('API deleteChatSession error:', error);
    throw error;
  }
};

/**
 * Delete / Clear all chat sessions
 */
export const clearAllChatSessions = async () => {
  try {
    const response = await apiClient.delete('/chat/sessions');
    return response.data;
  } catch (error) {
    console.error('API clearAllChatSessions error:', error);
    throw error;
  }
};


/**
 * Tourism information endpoints
 */
export const fetchTouristPlaces = async (params = {}) => {
  const res = await apiClient.get('/tourist-places', { params });
  return res.data;
};

export const fetchHotels = async (params = {}) => {
  const res = await apiClient.get('/hotels', { params });
  return res.data;
};

export const fetchRestaurants = async (params = {}) => {
  const res = await apiClient.get('/restaurants', { params });
  return res.data;
};

export const fetchEvents = async (params = {}) => {
  const res = await apiClient.get('/events', { params });
  return res.data;
};

export const fetchCategories = async () => {
  const res = await apiClient.get('/categories');
  return res.data;
};

export default {
  sendMessage,
  fetchChatSessions,
  fetchChatSession,
  deleteChatSession,
  fetchTouristPlaces,
  fetchHotels,
  fetchRestaurants,
  fetchEvents,
  fetchCategories,
};
