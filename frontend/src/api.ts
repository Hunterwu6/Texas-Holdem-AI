import axios from 'axios';
import { GameState, CreateGameRequest, PlayerActionRequest } from './types';

const API_BASE_URL =
  (import.meta.env?.VITE_API_URL as string | undefined) ?? 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const gameApi = {
  createGame: async (request: CreateGameRequest): Promise<GameState> => {
    const response = await api.post<GameState>('/api/games', request);
    return response.data;
  },

  getGame: async (gameId: string): Promise<GameState> => {
    const response = await api.get<GameState>(`/api/games/${gameId}`);
    return response.data;
  },

  startHand: async (gameId: string): Promise<GameState> => {
    const response = await api.post<GameState>(`/api/games/${gameId}/start`);
    return response.data;
  },

  submitAction: async (gameId: string, action: PlayerActionRequest): Promise<GameState> => {
    const response = await api.post<GameState>(`/api/games/${gameId}/action`, action);
    return response.data;
  },

  listGames: async () => {
    const response = await api.get('/api/games');
    return response.data;
  },

  getAIStrategies: async (): Promise<{strategies: string[]}> => {
    const response = await api.get('/api/ai/strategies');
    return response.data;
  },

  advanceAI: async (gameId: string): Promise<GameState> => {
    const response = await api.post<GameState>(`/api/games/${gameId}/advance`);
    return response.data;
  },

  updateLLMKeys: async (keys: {
    openai: string;
    deepseek: string;
    anthropic: string;
    gemini: string;
    grok: string;
  }): Promise<void> => {
    await api.post('/api/llm/configure', keys);
  },
};

export default api;

