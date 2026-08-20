import api from './api';

export const chatService = {
  /**
   * Send chat message to Angkor Verse AI assistant
   * Supports both object payload ({ message, language, session_id, history })
   * and (chatId, messageText) pattern from tourism-frontend.
   */
  async sendMessage(payloadOrChatId, maybeMessageText) {
    if (typeof payloadOrChatId === 'object') {
      return await api.post('/chat', payloadOrChatId);
    }
    return await api.post(`/chats/${payloadOrChatId}/messages`, {
      message_text: maybeMessageText || '',
    });
  },

  /**
   * Get all chats / active sessions
   */
  async getChats(params = {}) {
    const res = await api.get('/chats', { params });
    return res?.data ?? res;
  },

  /**
   * Get all chat sessions (compatibility endpoint)
   */
  async getChatSessions() {
    const res = await api.get('/chat/sessions');
    return res?.data ?? res;
  },

  /**
   * Get chat by ID or session ID
   */
  async getChatById(id) {
    const res = await api.get(`/chat/sessions/${id}`);
    return res?.data ?? res;
  },

  /**
   * Create a new chat conversation
   */
  async createChat(data) {
    return await api.post('/chats', data);
  },

  /**
   * Delete specific chat session
   */
  async deleteChatSession(sessionId) {
    return await api.delete(`/chat/sessions/${sessionId}`);
  },

  /**
   * Clear all chat sessions
   */
  async clearAllChatSessions() {
    return await api.delete('/chat/sessions');
  },

  /**
   * Update chat status
   */
  async updateStatus(chatId, data) {
    return await api.put(`/chats/${chatId}/status`, data);
  },

  /**
   * Tourism data endpoints
   */
  async getTouristPlaces(params = {}) {
    const res = await api.get('/tourist-places', { params });
    return res?.data ?? res;
  },

  async getPlaces(params = {}) {
    const res = await api.get('/places', { params });
    return res?.data ?? res;
  },

  async getHotels(params = {}) {
    const res = await api.get('/hotels', { params });
    return res?.data ?? res;
  },

  async getRestaurants(params = {}) {
    const res = await api.get('/restaurants', { params });
    return res?.data ?? res;
  },

  async getEvents(params = {}) {
    const res = await api.get('/events', { params });
    return res?.data ?? res;
  },

  async getRecommendations(data) {
    const res = await api.post('/recommendations', data);
    return res?.data ?? res;
  },

  async getItinerary(data) {
    const res = await api.post('/itineraries', data);
    return res?.data ?? res;
  },

  async getWeather(province, days = 3) {
    const res = await api.get('/weather', { params: { province, days } });
    return res?.data ?? res;
  },

  async getCurrency() {
    const res = await api.get('/currency');
    return res?.data ?? res;
  },

  async getSystemStatus() {
    const res = await api.get('/system/status');
    return res?.data ?? res;
  },
};

// Standalone function exports for direct imports
export const sendMessage = (payload) => chatService.sendMessage(payload);
export const fetchChatSessions = () => chatService.getChatSessions();
export const fetchChatSession = (id) => chatService.getChatById(id);
export const deleteChatSession = (id) => chatService.deleteChatSession(id);
export const clearAllChatSessions = () => chatService.clearAllChatSessions();
export const fetchTouristPlaces = (params) => chatService.getTouristPlaces(params);
export const fetchHotels = (params) => chatService.getHotels(params);
export const fetchRestaurants = (params) => chatService.getRestaurants(params);
export const fetchEvents = (params) => chatService.getEvents(params);
export const fetchCategories = () => chatService.getCategories();
export const fetchRecommendations = (data) => chatService.getRecommendations(data);
export const fetchItinerary = (data) => chatService.getItinerary(data);
export const fetchWeather = (province, days) => chatService.getWeather(province, days);
export const fetchCurrency = () => chatService.getCurrency();
export const fetchSystemStatus = () => chatService.getSystemStatus();

export default chatService;
