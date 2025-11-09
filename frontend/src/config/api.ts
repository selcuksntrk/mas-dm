/**
 * API configuration and constants
 */

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

export const API_ENDPOINTS = {
  HEALTH: '/health',
  DECISION_START: '/decisions/start',
  DECISION_STATUS: (processId: string) => `/decisions/status/${processId}`,
  DECISION_PROCESSES: '/decisions/processes',
  DECISION_CLEANUP: '/decisions/cleanup',
} as const;

export const POLLING_INTERVAL = 2000; // 2 seconds (matching backend recommendation)
export const MAX_POLL_ATTEMPTS = 300; // 10 minutes maximum (300 * 2s)
export const REQUEST_TIMEOUT = 30000; // 30 seconds
