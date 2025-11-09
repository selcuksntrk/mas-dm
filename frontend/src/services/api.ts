import axios, { AxiosError } from 'axios';
import { API_BASE_URL, REQUEST_TIMEOUT } from '@/config/api';
import type { DecisionRequest, DecisionResponse, ProcessState } from '@/types/decision';

/**
 * Axios instance with default configuration for /decisions routes
 */
const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/decisions`,  // Points to /api/decisions (proxied to backend:8001/decisions)
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: REQUEST_TIMEOUT,
});

/**
 * API error handler
 */
export class ApiError extends Error {
  statusCode?: number;
  originalError?: AxiosError;

  constructor(
    message: string,
    statusCode?: number,
    originalError?: AxiosError
  ) {
    super(message);
    this.name = 'ApiError';
    this.statusCode = statusCode;
    this.originalError = originalError;
  }
}

/**
 * Handle API errors consistently
 */
function handleApiError(error: unknown): never {
  if (axios.isAxiosError(error)) {
    const message = error.response?.data?.detail || error.message;
    throw new ApiError(message, error.response?.status, error);
  }
  throw new ApiError('An unexpected error occurred');
}

/**
 * API service methods
 */
export const decisionApi = {
  /**
   * Start a new decision process (async)
   */
  /**
   * Create a new decision process
   */
  async createDecision(request: DecisionRequest): Promise<DecisionResponse> {
    try {
      const response = await apiClient.post<DecisionResponse>(
        '/start',  // Backend endpoint is /decisions/start
        request
      );
      return response.data;
    } catch (error) {
      return handleApiError(error);
    }
  },

  /**
   * Get the status of a decision process
   */
  async getDecisionStatus(processId: string): Promise<ProcessState> {
    try {
      const response = await apiClient.get<ProcessState>(
        `/status/${processId}`  // Backend endpoint is /decisions/status/:id
      );
      return response.data;
    } catch (error) {
      return handleApiError(error);
    }
  },

  /**
   * Check API health
   */
  async checkHealth(): Promise<{ status: string }> {
    try {
      // Health is at root /health, not /decisions/health
      const response = await axios.get(`${API_BASE_URL}/health`, { timeout: REQUEST_TIMEOUT });
      return response.data;
    } catch (error) {
      return handleApiError(error);
    }
  },
};

export default apiClient;
