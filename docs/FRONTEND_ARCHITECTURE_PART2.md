# Frontend Architecture Guide - Part 2

## State Management Strategy

### Context-Based State Management

```typescript
// src/context/DecisionContext.tsx

import { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { decisionService } from '@/services/decisionService';
import type { DecisionResponse, ProcessStatus } from '@/types';

interface DecisionContextType {
  // State
  processId: string | null;
  status: ProcessStatus;
  results: DecisionResponse | null;
  error: string | null;
  
  // Actions
  startDecision: (query: string) => Promise<void>;
  resetDecision: () => void;
  
  // Computed
  isProcessing: boolean;
  progress: number;
}

const DecisionContext = createContext<DecisionContextType | null>(null);

export function DecisionProvider({ children }: { children: ReactNode }) {
  const [processId, setProcessId] = useState<string | null>(null);
  const [results, setResults] = useState<DecisionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Mutation to start decision process
  const startMutation = useMutation({
    mutationFn: decisionService.startDecision,
    onSuccess: (data) => {
      setProcessId(data.process_id);
      setError(null);
    },
    onError: (err: Error) => {
      setError(err.message);
    },
  });

  // Query to poll status (only when processId exists)
  const statusQuery = useQuery({
    queryKey: ['decision-status', processId],
    queryFn: () => decisionService.getStatus(processId!),
    enabled: !!processId && !results,
    refetchInterval: (data) => {
      // Stop polling when completed or failed
      if (data?.status === 'completed' || data?.status === 'failed') {
        return false;
      }
      // Poll every 2 seconds while running
      return 2000;
    },
    onSuccess: (data) => {
      if (data.status === 'completed' && data.result) {
        setResults(data.result);
      } else if (data.status === 'failed') {
        setError(data.error || 'Process failed');
      }
    },
  });

  const startDecision = useCallback(
    async (query: string) => {
      setResults(null);
      setError(null);
      await startMutation.mutateAsync(query);
    },
    [startMutation]
  );

  const resetDecision = useCallback(() => {
    setProcessId(null);
    setResults(null);
    setError(null);
  }, []);

  // Calculate progress based on status
  const progress = useMemo(() => {
    if (!processId) return 0;
    if (results) return 100;
    if (statusQuery.data?.status === 'running') return 50;
    if (statusQuery.data?.status === 'pending') return 10;
    return 0;
  }, [processId, results, statusQuery.data]);

  const value: DecisionContextType = {
    processId,
    status: statusQuery.data?.status || 'idle',
    results,
    error,
    startDecision,
    resetDecision,
    isProcessing: startMutation.isPending || statusQuery.isFetching,
    progress,
  };

  return (
    <DecisionContext.Provider value={value}>
      {children}
    </DecisionContext.Provider>
  );
}

// Custom hook for consuming context
export function useDecision() {
  const context = useContext(DecisionContext);
  if (!context) {
    throw new Error('useDecision must be used within DecisionProvider');
  }
  return context;
}
```

### Why This Pattern?

```typescript
/**
 * BENEFITS OF CONTEXT + REACT QUERY:
 * 
 * 1. AUTOMATIC POLLING
 *    React Query handles polling logic automatically
 *    No need for setInterval/setTimeout
 * 
 * 2. CACHING
 *    Results are cached by queryKey
 *    Switching tabs and back? Data is still there
 * 
 * 3. DEDUPLICATION
 *    Multiple components calling same query?
 *    Only one network request is made
 * 
 * 4. LOADING STATES
 *    React Query tracks isPending, isError, etc.
 *    No need for separate loading state variables
 * 
 * 5. ERROR HANDLING
 *    Automatic retry logic
 *    Error boundaries integration
 * 
 * 6. OPTIMISTIC UPDATES
 *    Can update UI before API responds
 *    Rolls back if API fails
 */

// ALTERNATIVE APPROACH (without React Query):
// 
// Would need to manually:
// - Set up polling with setInterval
// - Track loading states
// - Handle cleanup (clearInterval)
// - Implement retry logic
// - Cache responses
// - Handle race conditions
// 
// React Query does all this for us! 🎉
```

---

## Real-Time Updates & Polling

### Smart Polling Strategy

```typescript
// src/hooks/useProcessStatus.ts

import { useQuery } from '@tanstack/react-query';
import { decisionService } from '@/services/decisionService';

interface UseProcessStatusOptions {
  processId: string | null;
  onComplete?: (result: DecisionResponse) => void;
  onError?: (error: string) => void;
}

export function useProcessStatus({
  processId,
  onComplete,
  onError,
}: UseProcessStatusOptions) {
  const query = useQuery({
    queryKey: ['process-status', processId],
    queryFn: () => decisionService.getStatus(processId!),
    enabled: !!processId,
    
    // SMART POLLING LOGIC
    refetchInterval: (data, query) => {
      // Stop polling if no data yet
      if (!data) return false;
      
      // Stop polling on completion
      if (data.status === 'completed') {
        onComplete?.(data.result!);
        return false;
      }
      
      // Stop polling on failure
      if (data.status === 'failed') {
        onError?.(data.error || 'Unknown error');
        return false;
      }
      
      // Adaptive polling interval based on status
      if (data.status === 'pending') {
        return 5000;  // Poll slowly when pending (5 seconds)
      }
      
      if (data.status === 'running') {
        return 2000;  // Poll frequently when running (2 seconds)
      }
      
      return false;  // Stop polling for unknown states
    },
    
    // BACKGROUND REFETCHING
    refetchOnWindowFocus: true,   // Refetch when user returns to tab
    refetchOnReconnect: true,     // Refetch when internet reconnects
    
    // STALE TIME
    staleTime: 0,  // Always consider data stale (always refetch)
    
    // RETRY LOGIC
    retry: 3,                          // Retry failed requests 3 times
    retryDelay: (attemptIndex) => {
      return Math.min(1000 * 2 ** attemptIndex, 30000);  // Exponential backoff
    },
  });

  return query;
}

/**
 * WHY ADAPTIVE POLLING?
 * 
 * Different states need different polling frequencies:
 * 
 * PENDING (5 seconds):
 * - Process is queued but not started
 * - Not changing frequently
 * - No need to hammer the server
 * 
 * RUNNING (2 seconds):
 * - Process is actively executing
 * - User wants to see progress
 * - More frequent updates feel responsive
 * 
 * COMPLETED/FAILED (stop):
 * - Process is done
 * - No point in polling anymore
 * - Saves server resources
 * 
 * This approach:
 * ✓ Reduces unnecessary network requests
 * ✓ Improves perceived performance
 * ✓ Scales better with many users
 */
```

### WebSocket Alternative (Future Enhancement)

```typescript
/**
 * POLLING vs WEBSOCKETS
 * 
 * CURRENT: Polling (HTTP requests every 2-5 seconds)
 * ✓ Simple to implement
 * ✓ Works with existing REST API
 * ✓ No additional infrastructure needed
 * ✓ Works through firewalls/proxies
 * ✗ Higher latency (2-5 second delay)
 * ✗ More server load (many requests)
 * ✗ Wastes bandwidth (most polls return "no change")
 * 
 * FUTURE: WebSockets (real-time bidirectional connection)
 * ✓ Instant updates (< 100ms latency)
 * ✓ Lower server load (one connection per client)
 * ✓ Efficient (server pushes only when data changes)
 * ✗ More complex to implement
 * ✗ Requires WebSocket support on backend
 * ✗ Needs connection management (reconnection logic)
 * 
 * RECOMMENDATION:
 * - Start with polling (current approach)
 * - Migrate to WebSockets when:
 *   • You have many concurrent users (> 100)
 *   • Need sub-second latency
 *   • Want to reduce server costs
 */

// Example WebSocket implementation (future):
class ProcessWebSocket {
  private ws: WebSocket | null = null;
  private processId: string;
  
  connect(processId: string) {
    this.processId = processId;
    this.ws = new WebSocket(`ws://localhost:8001/ws/process/${processId}`);
    
    this.ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      // Handle real-time update
      this.onUpdate(update);
    };
    
    this.ws.onerror = () => {
      // Fallback to polling on WebSocket error
      this.fallbackToPolling();
    };
  }
  
  disconnect() {
    this.ws?.close();
  }
}
```

---

## Animation & Visual Feedback

### Animation Principles

```typescript
/**
 * ANIMATION GUIDELINES:
 * 
 * 1. PURPOSE
 *    Every animation should have a purpose:
 *    - Provide feedback (button clicked)
 *    - Show state change (loading → completed)
 *    - Guide attention (highlight new content)
 *    - Add delight (subtle micro-interactions)
 * 
 * 2. DURATION
 *    - Micro interactions: 100-200ms (button hover)
 *    - Small animations: 200-300ms (card appear)
 *    - Medium animations: 300-500ms (page transition)
 *    - Large animations: 500-800ms (modal open)
 *    - Never exceed 1 second (feels slow)
 * 
 * 3. EASING
 *    - ease-out: Things entering (starts fast, slows down)
 *    - ease-in: Things exiting (starts slow, speeds up)
 *    - ease-in-out: Moving between states
 *    - spring: Playful, bouncy (use sparingly)
 * 
 * 4. PERFORMANCE
 *    - Animate only: transform, opacity
 *    - Avoid: width, height, top, left (causes reflow)
 *    - Use: translateX, translateY, scale (GPU accelerated)
 * 
 * 5. ACCESSIBILITY
 *    - Respect prefers-reduced-motion
 *    - Provide option to disable animations
 *    - Don't rely solely on animation to convey information
 */
```

### Reusable Animation Components

```typescript
// src/components/animations/FadeIn.tsx

import { motion, HTMLMotionProps } from 'framer-motion';
import { ReactNode } from 'react';

interface FadeInProps extends HTMLMotionProps<'div'> {
  children: ReactNode;
  delay?: number;
  duration?: number;
  direction?: 'up' | 'down' | 'left' | 'right' | 'none';
}

export function FadeIn({
  children,
  delay = 0,
  duration = 0.3,
  direction = 'up',
  ...props
}: FadeInProps) {
  const directions = {
    up: { y: 20 },
    down: { y: -20 },
    left: { x: 20 },
    right: { x: -20 },
    none: {},
  };

  return (
    <motion.div
      initial={{ opacity: 0, ...directions[direction] }}
      animate={{ opacity: 1, x: 0, y: 0 }}
      transition={{
        duration,
        delay,
        ease: [0.25, 0.1, 0.25, 1],  // Custom easing curve
      }}
      {...props}
    >
      {children}
    </motion.div>
  );
}

// USAGE:
// <FadeIn>
//   <Card>Content appears smoothly</Card>
// </FadeIn>
//
// <FadeIn direction="left" delay={0.2}>
//   <Card>Slides in from left after 200ms</Card>
// </FadeIn>
```

```typescript
// src/components/animations/Stagger.tsx

import { motion } from 'framer-motion';
import { Children, ReactNode } from 'react';

interface StaggerProps {
  children: ReactNode;
  staggerDelay?: number;
  className?: string;
}

export function Stagger({
  children,
  staggerDelay = 0.1,
  className,
}: StaggerProps) {
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: staggerDelay,
      },
    },
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 },
  };

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className={className}
    >
      {Children.map(children, (child) => (
        <motion.div variants={item}>{child}</motion.div>
      ))}
    </motion.div>
  );
}

// USAGE:
// <Stagger staggerDelay={0.1}>
//   <NodeCard />  {/* Appears first */}
//   <NodeCard />  {/* Appears 0.1s later */}
//   <NodeCard />  {/* Appears 0.2s later */}
// </Stagger>
```

```typescript
// src/components/animations/PulseLoader.tsx

import { motion } from 'framer-motion';

interface PulseLoaderProps {
  size?: 'sm' | 'md' | 'lg';
  color?: string;
}

export function PulseLoader({ size = 'md', color = 'blue' }: PulseLoaderProps) {
  const sizes = {
    sm: 'w-2 h-2',
    md: 'w-3 h-3',
    lg: 'w-4 h-4',
  };

  const colors = {
    blue: 'bg-blue-600',
    gray: 'bg-gray-600',
    green: 'bg-green-600',
  };

  const dotVariants = {
    initial: { scale: 0.8, opacity: 0.5 },
    animate: { scale: 1.2, opacity: 1 },
  };

  return (
    <div className="flex items-center gap-2">
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          className={`rounded-full ${sizes[size]} ${colors[color]}`}
          variants={dotVariants}
          initial="initial"
          animate="animate"
          transition={{
            duration: 0.6,
            repeat: Infinity,
            repeatType: 'reverse',
            delay: i * 0.2,
          }}
        />
      ))}
    </div>
  );
}

// USAGE:
// <PulseLoader />  // Default (medium, blue)
// <PulseLoader size="lg" color="green" />
```

### Process Graph Animation

```typescript
// src/components/decision/ProcessGraph.tsx

import { motion, AnimatePresence } from 'framer-motion';
import { NodeCard } from './NodeCard';
import type { GraphNode } from '@/types';

interface ProcessGraphProps {
  nodes: GraphNode[];
  currentNodeId?: string;
}

export function ProcessGraph({ nodes, currentNodeId }: ProcessGraphProps) {
  return (
    <div className="space-y-4">
      <AnimatePresence mode="popLayout">
        {nodes.map((node, index) => {
          const isActive = node.id === currentNodeId;
          const isCompleted = node.status === 'completed';
          const isPending = node.status === 'pending';

          return (
            <motion.div
              key={node.id}
              layout  // Animate layout changes automatically
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{
                opacity: 1,
                scale: isActive ? 1.05 : 1,  // Slightly larger when active
              }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{
                layout: { duration: 0.3 },
                scale: { duration: 0.2 },
              }}
            >
              {/* Glow effect for active node */}
              {isActive && (
                <motion.div
                  className="absolute inset-0 -z-10 rounded-lg bg-blue-400 blur-xl"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 0.3 }}
                  exit={{ opacity: 0 }}
                />
              )}

              <NodeCard
                title={node.title}
                description={node.description}
                status={node.status}
                evaluationStatus={node.evaluationStatus}
                index={index}
              />

              {/* Connection line to next node */}
              {index < nodes.length - 1 && (
                <motion.div
                  className="h-8 w-0.5 mx-auto my-2"
                  initial={{ backgroundColor: '#e5e7eb' }}  // gray-200
                  animate={{
                    backgroundColor: isCompleted ? '#10b981' : '#e5e7eb',  // green-500 : gray-200
                  }}
                  transition={{ duration: 0.5 }}
                />
              )}
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
```

### Progress Animation

```typescript
// src/components/decision/ProgressBar.tsx

import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

interface ProgressBarProps {
  progress: number;  // 0-100
  status: 'pending' | 'running' | 'completed' | 'failed';
}

export function ProgressBar({ progress, status }: ProgressBarProps) {
  const [displayProgress, setDisplayProgress] = useState(0);

  // Smooth progress animation
  useEffect(() => {
    const timer = setTimeout(() => {
      setDisplayProgress(progress);
    }, 100);
    return () => clearTimeout(timer);
  }, [progress]);

  const statusColors = {
    pending: 'bg-gray-400',
    running: 'bg-blue-600',
    completed: 'bg-green-600',
    failed: 'bg-red-600',
  };

  const statusText = {
    pending: 'Initializing...',
    running: `Processing... ${Math.round(displayProgress)}%`,
    completed: 'Completed!',
    failed: 'Failed',
  };

  return (
    <div className="w-full space-y-2">
      {/* Progress bar */}
      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
        <motion.div
          className={`h-full ${statusColors[status]}`}
          initial={{ width: '0%' }}
          animate={{ width: `${displayProgress}%` }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        />
      </div>

      {/* Status text */}
      <div className="flex justify-between items-center text-sm">
        <span className="text-gray-600">{statusText[status]}</span>
        {status === 'running' && (
          <motion.span
            className="text-gray-500"
            animate={{ opacity: [1, 0.5, 1] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          >
            This may take 1-2 minutes
          </motion.span>
        )}
      </div>
    </div>
  );
}
```

---

## API Integration Patterns

### API Service Layer

```typescript
// src/services/api.ts

import axios, { AxiosError, AxiosInstance } from 'axios';
import { z } from 'zod';

// Create axios instance with default config
export const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001',
  timeout: 120000,  // 2 minutes (decision process can be slow)
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor (for logging, auth, etc.)
api.interceptors.request.use(
  (config) => {
    // Log requests in development
    if (import.meta.env.DEV) {
      console.log('[API Request]', config.method?.toUpperCase(), config.url);
    }
    
    // Add auth token if exists
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor (for error handling)
api.interceptors.response.use(
  (response) => {
    // Log responses in development
    if (import.meta.env.DEV) {
      console.log('[API Response]', response.status, response.config.url);
    }
    return response;
  },
  (error: AxiosError) => {
    // Handle errors globally
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const message = (error.response.data as any)?.detail || error.message;
      
      if (status === 401) {
        // Unauthorized - redirect to login
        window.location.href = '/login';
      } else if (status === 404) {
        console.error('[API] Resource not found:', message);
      } else if (status >= 500) {
        console.error('[API] Server error:', message);
      }
      
      return Promise.reject(new Error(message));
    } else if (error.request) {
      // Request made but no response
      console.error('[API] No response from server');
      return Promise.reject(new Error('Unable to connect to server'));
    } else {
      // Something else happened
      console.error('[API] Request error:', error.message);
      return Promise.reject(error);
    }
  }
);

/**
 * Type-safe API wrapper with Zod validation
 */
export async function apiRequest<T>(
  method: 'get' | 'post' | 'put' | 'delete',
  url: string,
  schema: z.ZodType<T>,
  data?: any
): Promise<T> {
  try {
    const response = await api[method](url, data);
    
    // Validate response with Zod
    const validated = schema.parse(response.data);
    
    return validated;
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error('[API] Response validation failed:', error.errors);
      throw new Error('Invalid response from server');
    }
    throw error;
  }
}
```

### Decision Service

```typescript
// src/services/decisionService.ts

import { z } from 'zod';
import { api, apiRequest } from './api';

// Zod schemas for validation
const ProcessStartResponseSchema = z.object({
  process_id: z.string(),
  status: z.string(),
  message: z.string(),
});

const ProcessStatusResponseSchema = z.object({
  process_id: z.string(),
  status: z.enum(['pending', 'running', 'completed', 'failed']),
  created_at: z.string().optional(),
  completed_at: z.string().optional(),
  result: z.object({
    selected_decision: z.string(),
    selected_decision_comment: z.string(),
    alternative_decision: z.string(),
    alternative_decision_comment: z.string(),
    trigger: z.string().default(''),
    root_cause: z.string().default(''),
    scope_definition: z.string().default(''),
    decision_drafted: z.string().default(''),
    goals: z.string().default(''),
    complementary_info: z.string().default(''),
    decision_draft_updated: z.string().default(''),
    alternatives: z.string().default(''),
  }).optional(),
  error: z.string().optional(),
});

const DecisionResponseSchema = ProcessStatusResponseSchema.shape.result!;

// Export types inferred from schemas
export type ProcessStartResponse = z.infer<typeof ProcessStartResponseSchema>;
export type ProcessStatusResponse = z.infer<typeof ProcessStatusResponseSchema>;
export type DecisionResponse = z.infer<typeof DecisionResponseSchema>;

/**
 * Decision API Service
 * 
 * Handles all communication with the decision-making backend.
 */
export const decisionService = {
  /**
   * Start a new decision-making process
   */
  async startDecision(query: string): Promise<ProcessStartResponse> {
    return apiRequest(
      'post',
      '/decisions/start',
      ProcessStartResponseSchema,
      { decision_query: query }
    );
  },

  /**
   * Get the status of a running process
   */
  async getStatus(processId: string): Promise<ProcessStatusResponse> {
    return apiRequest(
      'get',
      `/decisions/status/${processId}`,
      ProcessStatusResponseSchema
    );
  },

  /**
   * Run a decision synchronously (blocks until complete)
   * Use this only for testing or when you can wait.
   */
  async runDecisionSync(query: string): Promise<DecisionResponse> {
    return apiRequest(
      'post',
      '/decisions/run',
      DecisionResponseSchema,
      { decision_query: query }
    );
  },

  /**
   * Get list of all processes
   */
  async listProcesses() {
    const response = await api.get('/decisions/processes');
    return response.data;
  },

  /**
   * Clean up completed processes
   */
  async cleanup() {
    const response = await api.delete('/decisions/cleanup');
    return response.data;
  },
};

/**
 * WHY ZOD VALIDATION?
 * 
 * TypeScript only validates at compile time:
 * 
 * interface Response {
 *   process_id: string;
 * }
 * 
 * const data: Response = await api.get('/...');
 * // TypeScript: "I trust this is a Response" ✗
 * // Reality: API might return { processId: 123 } (wrong!)
 * 
 * Zod validates at runtime:
 * 
 * const data = ProcessStartResponseSchema.parse(await api.get('/...'));
 * // Zod: "I verified this matches the schema" ✓
 * // If not, throws descriptive error
 * 
 * Benefits:
 * ✓ Catch API contract changes immediately
 * ✓ Type safety at runtime, not just compile time
 * ✓ Better error messages
 * ✓ Auto-complete still works (inferred types)
 */
```

---

## Error Handling & Loading States

### Error Boundary

```typescript
// src/components/ErrorBoundary.tsx

import { Component, ErrorInfo, ReactNode } from 'react';
import { Button } from './ui/Button';
import { AlertTriangle } from 'lucide-react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log to error reporting service (e.g., Sentry)
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="min-h-screen flex items-center justify-center p-4">
          <div className="max-w-md w-full text-center space-y-4">
            <AlertTriangle className="w-12 h-12 text-red-500 mx-auto" />
            <h1 className="text-2xl font-bold text-gray-900">
              Something went wrong
            </h1>
            <p className="text-gray-600">
              {this.state.error?.message || 'An unexpected error occurred'}
            </p>
            <Button
              onClick={() => window.location.reload()}
              variant="primary"
            >
              Reload Page
            </Button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

// USAGE in App.tsx:
// <ErrorBoundary>
//   <App />
// </ErrorBoundary>
```

### Loading States

```typescript
// src/components/LoadingState.tsx

import { Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

interface LoadingStateProps {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
}

export function LoadingState({
  message = 'Loading...',
  size = 'md',
}: LoadingStateProps) {
  const sizes = {
    sm: 'w-6 h-6',
    md: 'w-10 h-10',
    lg: 'w-16 h-16',
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="flex flex-col items-center justify-center p-8 space-y-4"
    >
      <Loader2 className={`${sizes[size]} text-blue-600 animate-spin`} />
      <p className="text-gray-600">{message}</p>
    </motion.div>
  );
}

// Skeleton loader for cards
export function SkeletonCard() {
  return (
    <div className="animate-pulse space-y-4">
      <div className="h-4 bg-gray-200 rounded w-3/4"></div>
      <div className="space-y-2">
        <div className="h-3 bg-gray-200 rounded"></div>
        <div className="h-3 bg-gray-200 rounded w-5/6"></div>
      </div>
    </div>
  );
}
```

### Error Display

```typescript
// src/components/ErrorDisplay.tsx

import { AlertCircle, XCircle } from 'lucide-react';
import { Button } from './ui/Button';

interface ErrorDisplayProps {
  title?: string;
  message: string;
  onRetry?: () => void;
  onDismiss?: () => void;
}

export function ErrorDisplay({
  title = 'Error',
  message,
  onRetry,
  onDismiss,
}: ErrorDisplayProps) {
  return (
    <div className="rounded-lg border-2 border-red-200 bg-red-50 p-4">
      <div className="flex items-start gap-3">
        <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-semibold text-red-900">{title}</h3>
          <p className="mt-1 text-sm text-red-700">{message}</p>
          {(onRetry || onDismiss) && (
            <div className="mt-3 flex gap-2">
              {onRetry && (
                <Button size="sm" variant="secondary" onClick={onRetry}>
                  Try Again
                </Button>
              )}
              {onDismiss && (
                <Button size="sm" variant="ghost" onClick={onDismiss}>
                  Dismiss
                </Button>
              )}
            </div>
          )}
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="flex-shrink-0 text-red-600 hover:text-red-800"
          >
            <XCircle className="w-5 h-5" />
          </button>
        )}
      </div>
    </div>
  );
}
```

---

*This concludes Part 2. Would you like me to continue with Part 3 covering Performance Optimization, Testing Strategy, Deployment, and the Development Roadmap?*
