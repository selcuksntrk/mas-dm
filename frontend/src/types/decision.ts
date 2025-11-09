/**
 * Domain models matching backend structure
 */

export interface DecisionRequest {
  decision_query: string;  // Backend expects 'decision_query', not 'query'
}

export interface DecisionResponse {
  process_id: string;
  status: string;
  message: string;
}

export interface ProcessState {
  process_id: string;
  // Backend uses 'running' for in-progress processes; allow both for compatibility
  status: 'pending' | 'running' | 'processing' | 'completed' | 'failed';
  created_at: string;
  completed_at?: string;
  result?: DecisionResult;
  error?: string;
}

export interface DecisionResult {
  selected_decision: string;
  selected_decision_comment: string;
  alternative_decision: string;
  alternative_decision_comment: string;
  trigger: string;
  root_cause: string;
  scope_definition: string;
  decision_drafted: string;
  goals: string;
  complementary_info?: string;
  decision_draft_updated?: string;
  alternatives?: string;
}

export interface GraphNode {
  id: string;
  label: string;
  type: 'start' | 'decision' | 'evaluator' | 'final';
  // Accept 'running' from backend as an in-progress state
  status: 'pending' | 'running' | 'processing' | 'completed' | 'failed';
  data?: unknown;
}

export interface GraphEdge {
  from: string;
  to: string;
}
