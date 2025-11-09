import { useMutation, useQuery } from '@tanstack/react-query';
import { decisionApi } from '@/services/api';
import { POLLING_INTERVAL } from '@/config/api';
import type { DecisionRequest, ProcessState } from '@/types/decision';

/**
 * Hook to create a new decision process
 */
export function useCreateDecision() {
  return useMutation({
    mutationFn: (request: DecisionRequest) => decisionApi.createDecision(request),
  });
}

/**
 * Hook to poll decision process status
 * Automatically refetches every 2 seconds while process is active
 */
export function useDecisionStatus(processId: string | null, enabled = true) {
  return useQuery({
    queryKey: ['decision-status', processId],
    queryFn: () => decisionApi.getDecisionStatus(processId!),
    enabled: enabled && !!processId,
      refetchInterval: (query) => {
        const data = query.state.data as ProcessState | undefined;
        // Keep polling while running/processing or pending
        if (data?.status === 'running' || data?.status === 'processing' || data?.status === 'pending') {
          return POLLING_INTERVAL; // Poll interval from config
        }
        return false; // Stop polling when completed/failed
      },
    staleTime: 0, // Always consider data stale to enable polling
    retry: 3,
    retryDelay: 1000,
  });
}

/**
 * Hook to check API health
 */
export function useApiHealth() {
  return useQuery({
    queryKey: ['api-health'],
    queryFn: () => decisionApi.checkHealth(),
    refetchInterval: 30000, // Check every 30 seconds
    retry: 3,
    staleTime: 10000, // Consider fresh for 10 seconds
  });
}
