import { useMemo } from 'react';
import type { ProcessState, GraphNode, GraphEdge } from '@/types/decision';

/**
 * Hook to transform ProcessState into graph data structure
 * Simplified version for backend process visualization
 */
export function useProcessGraph(processState: ProcessState | undefined) {
  return useMemo(() => {
    if (!processState) {
      return { nodes: [], edges: [] };
    }

    const nodes: GraphNode[] = [];
    const edges: GraphEdge[] = [];

    // Determine overall status for all nodes
    const isCompleted = processState.status === 'completed';
    const isFailed = processState.status === 'failed';
    const isRunning = processState.status === 'running';

    // Start node
    nodes.push({
      id: 'start',
      label: 'Decision Query',
      type: 'start',
      status: 'completed',
    });

    // Main process phases based on backend flow
    const phases = [
      { id: 'trigger', label: 'Identify Trigger', order: 1 },
      { id: 'root-cause', label: 'Root Cause Analysis', order: 2 },
      { id: 'scope', label: 'Define Scope', order: 3 },
      { id: 'draft', label: 'Draft Decision', order: 4 },
      { id: 'goals', label: 'Define Goals', order: 5 },
      { id: 'alternatives', label: 'Generate Alternatives', order: 6 },
      { id: 'selection', label: 'Select Decision', order: 7 },
    ];

    phases.forEach((phase, index) => {
      let status: GraphNode['status'] = 'pending';
      
      if (isFailed) {
        status = index === 0 ? 'failed' : 'pending';
      } else if (isCompleted) {
        status = 'completed';
      } else if (isRunning) {
        // Show first few as completed, current as processing, rest as pending
        status = index < 3 ? 'completed' : index === 3 ? 'processing' : 'pending';
      }

      nodes.push({
        id: phase.id,
        label: phase.label,
        type: 'decision',
        status,
      });

      // Add edges
      const fromId = index === 0 ? 'start' : phases[index - 1].id;
      edges.push({
        from: fromId,
        to: phase.id,
      });
    });

    // Final node
    nodes.push({
      id: 'final',
      label: 'Final Decision',
      type: 'final',
      status: isCompleted ? 'completed' : isFailed ? 'failed' : 'pending',
    });

    edges.push({
      from: phases[phases.length - 1].id,
      to: 'final',
    });

    return { nodes, edges };
  }, [processState]);
}
