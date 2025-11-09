# Frontend Architecture Diagrams

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER BROWSER                                │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    REACT APPLICATION                          │  │
│  │                                                               │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │  │
│  │  │ Decision     │  │  Process     │  │   Results    │      │  │
│  │  │ Form         │→ │  Viewer      │→ │   Display    │      │  │
│  │  │              │  │              │  │              │      │  │
│  │  │ • Input      │  │ • Graph      │  │ • Selected   │      │  │
│  │  │ • Validate   │  │ • Progress   │  │ • Alternative│      │  │
│  │  │ • Submit     │  │ • Polling    │  │ • Details    │      │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘      │  │
│  │                                                               │  │
│  │  ┌──────────────────────────────────────────────────────┐   │  │
│  │  │           STATE MANAGEMENT (React Context)           │   │  │
│  │  │  • processId                                         │   │  │
│  │  │  • status (idle/running/completed)                   │   │  │
│  │  │  • results                                            │   │  │
│  │  │  • error                                              │   │  │
│  │  └──────────────────────────────────────────────────────┘   │  │
│  │                                                               │  │
│  │  ┌──────────────────────────────────────────────────────┐   │  │
│  │  │           DATA LAYER (React Query)                   │   │  │
│  │  │  • Automatic polling (every 2 seconds)               │   │  │
│  │  │  • Caching                                            │   │  │
│  │  │  • Error retry                                        │   │  │
│  │  └──────────────────────────────────────────────────────┘   │  │
│  │                                                               │  │
│  │  ┌──────────────────────────────────────────────────────┐   │  │
│  │  │           API SERVICE (Axios + Zod)                  │   │  │
│  │  │  • startDecision(query)                              │   │  │
│  │  │  • getStatus(processId)                              │   │  │
│  │  │  • Runtime validation                                 │   │  │
│  │  └──────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                       │
│                              ↕ HTTP/REST                             │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                         BACKEND API (FastAPI)                        │
│                                                                       │
│  POST /decisions/start      → Start new decision process            │
│  GET  /decisions/status/:id → Get process status and result         │
│  GET  /graph/structure      → Get agent graph structure             │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                   MULTI-AGENT SYSTEM                          │  │
│  │                                                               │  │
│  │  Agent 1: Identify Trigger                                   │  │
│  │  Agent 2: Root Cause Analysis                                │  │
│  │  Agent 3: Scope Definition                                   │  │
│  │  Agent 4: Draft Decision                                     │  │
│  │  Agent 5: Establish Goals                                    │  │
│  │  Agent 6: Information Needs                                  │  │
│  │  Agent 7: Retrieve Information                               │  │
│  │  Agent 8: Update Draft                                       │  │
│  │  Agent 9: Generate Alternatives                              │  │
│  │  Agent 10: Compile Results                                   │  │
│  │                                                               │  │
│  │  + 9 Evaluator Agents (one for each phase)                   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    REDIS PERSISTENCE                          │  │
│  │  • Process metadata                                           │  │
│  │  • Decision results                                           │  │
│  │  • Status tracking                                            │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Tree

```
App
│
├─ ErrorBoundary
│  └─ CatchAll errors
│
├─ QueryClientProvider (React Query)
│  └─ Handles all API calls & caching
│
└─ DecisionProvider (Context)
   └─ Global state management
      │
      └─ Router
         │
         ├─ HomePage (/)
         │  │
         │  ├─ Header
         │  │  └─ Logo + Title
         │  │
         │  └─ Container
         │     │
         │     ├─ DecisionForm (when idle)
         │     │  ├─ FadeIn animation
         │     │  ├─ TextArea (query input)
         │     │  ├─ Button (submit)
         │     │  └─ ErrorDisplay (if error)
         │     │
         │     ├─ ProcessVisualization (when running)
         │     │  ├─ ProgressBar
         │     │  │  ├─ AnimatedBar
         │     │  │  └─ StatusText
         │     │  │
         │     │  ├─ StatusMessage
         │     │  │  └─ PulseLoader
         │     │  │
         │     │  └─ ProcessGraph
         │     │     └─ Stagger animation
         │     │        └─ NodeCard (x10+)
         │     │           ├─ StatusIcon
         │     │           │  ├─ Pending (gray circle)
         │     │           │  ├─ Running (blue spinner)
         │     │           │  ├─ Completed (green check)
         │     │           │  └─ Failed (red X)
         │     │           ├─ NodeTitle
         │     │           ├─ NodeDescription
         │     │           └─ EvaluationBadge
         │     │              ├─ "✓ Evaluated" (if correct)
         │     │              └─ "⚠ Evaluated" (if incorrect)
         │     │
         │     └─ ResultsDisplay (when completed)
         │        ├─ SlideIn animation
         │        │
         │        ├─ DecisionCard (primary)
         │        │  ├─ CardHeader
         │        │  │  ├─ CardTitle: "Selected Decision"
         │        │  │  └─ Badge: "Recommended"
         │        │  ├─ CardContent
         │        │  │  └─ Decision text
         │        │  └─ CardFooter
         │        │     └─ Comment/reasoning
         │        │
         │        ├─ AlternativeCard (secondary)
         │        │  ├─ CardHeader
         │        │  │  └─ CardTitle: "Alternative"
         │        │  ├─ CardContent
         │        │  │  └─ Alternative text
         │        │  └─ CardFooter
         │        │     └─ Comment/reasoning
         │        │
         │        └─ ProcessAccordion
         │           ├─ AccordionItem: Trigger
         │           ├─ AccordionItem: Root Cause
         │           ├─ AccordionItem: Scope
         │           ├─ AccordionItem: Goals
         │           ├─ AccordionItem: Information
         │           └─ AccordionItem: Alternatives
         │
         └─ Footer
            └─ Credits + Links
```

## Data Flow

### Starting a Decision

```
User Action: Submit Query
         ↓
┌────────────────────────┐
│  DecisionForm          │
│  handleSubmit()        │
└──────────┬─────────────┘
           │ validates input
           ↓
┌────────────────────────┐
│  useDecision() hook    │
│  startDecision(query)  │
└──────────┬─────────────┘
           │ mutation
           ↓
┌────────────────────────┐
│  React Query           │
│  useMutation           │
└──────────┬─────────────┘
           │ POST request
           ↓
┌────────────────────────┐
│  decisionService.ts    │
│  startDecision(query)  │
└──────────┬─────────────┘
           │ axios.post()
           ↓
┌────────────────────────┐
│  API (Axios)           │
│  + Zod validation      │
└──────────┬─────────────┘
           │ HTTP POST
           ↓
┌────────────────────────┐
│  Backend API           │
│  /decisions/start      │
└──────────┬─────────────┘
           │ returns
           │ { process_id, status }
           ↓
┌────────────────────────┐
│  Context updates       │
│  setProcessId(id)      │
└──────────┬─────────────┘
           │ triggers
           ↓
┌────────────────────────┐
│  React Query           │
│  useQuery (polling)    │
└────────────────────────┘
```

### Polling for Status

```
┌────────────────────────┐
│  React Query           │
│  useQuery enabled      │
└──────────┬─────────────┘
           │ every 2 seconds
           ↓
┌────────────────────────┐
│  decisionService.ts    │
│  getStatus(processId)  │
└──────────┬─────────────┘
           │ axios.get()
           ↓
┌────────────────────────┐
│  Backend API           │
│  /decisions/status/:id │
└──────────┬─────────────┘
           │ returns status
           ↓
┌────────────────────────┐
│  Status Check          │
│  if completed → stop   │
│  if failed → stop      │
│  if running → continue │
└──────────┬─────────────┘
           │ updates UI
           ↓
┌────────────────────────┐
│  ProcessGraph          │
│  highlights active node│
└────────────────────────┘
```

### Displaying Results

```
Backend: status = "completed"
         result = { ... }
              ↓
React Query: onSuccess callback
              ↓
Context: setResults(result)
              ↓
Component: useDecision()
              ↓
ResultsDisplay: renders
              ↓
Framer Motion: animates
```

## State Flow

```
┌─────────────────────────────────────────────────────────┐
│                    APPLICATION STATE                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  GLOBAL STATE (DecisionContext)                │    │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │    │
│  │  processId: string | null                      │    │
│  │  status: 'idle' | 'pending' | 'running' |      │    │
│  │          'completed' | 'failed'                │    │
│  │  results: DecisionResponse | null              │    │
│  │  error: string | null                          │    │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │    │
│  │  startDecision(query): Promise<void>           │    │
│  │  resetDecision(): void                         │    │
│  └────────────────────────────────────────────────┘    │
│                        ↕                                 │
│  ┌────────────────────────────────────────────────┐    │
│  │  SERVER STATE (React Query)                    │    │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │    │
│  │  Cached API responses                          │    │
│  │  Loading states                                │    │
│  │  Error states                                  │    │
│  │  Automatic refetching                          │    │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │    │
│  │  useQuery(['status', processId])               │    │
│  │  useMutation(startDecision)                    │    │
│  └────────────────────────────────────────────────┘    │
│                        ↕                                 │
│  ┌────────────────────────────────────────────────┐    │
│  │  LOCAL COMPONENT STATE                         │    │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │    │
│  │  Form inputs (useState)                        │    │
│  │  UI toggles (useState)                         │    │
│  │  Animation states (Framer Motion)              │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Animation Timeline

### Node Card Animation Sequence

```
TIME →
─────┬───────┬───────┬───────┬───────┬───────┬───────┬────
     0ms   100ms  200ms  300ms  400ms  500ms  600ms

Node 1:  [fade in + slide up]
           │
           └─ opacity: 0→1, y: 20→0

Node 2:     [delay 100ms] [fade in + slide up]
                 │
                 └─ opacity: 0→1, y: 20→0

Node 3:          [delay 200ms] [fade in + slide up]
                      │
                      └─ opacity: 0→1, y: 20→0

Result: Staggered entrance effect (100ms between each node)
```

### Active Node Pulse Animation

```
LOOP (2 seconds):

0.0s  ━━━━━━━━━  Normal state
      [scale: 1, shadow: 0]

0.5s  ━━━━━━━━━  Scale up start
      [scale: 1→1.05]

1.0s  ━━━━━━━━━  Maximum scale + shadow
      [scale: 1.05, shadow: 10px blue]

1.5s  ━━━━━━━━━  Scale down
      [scale: 1.05→1]

2.0s  ━━━━━━━━━  Back to normal
      [scale: 1, shadow: 0]
      → Repeat
```

### Results Appear Animation

```
Before: Results are completed
        [opacity: 0, x: 50, off-screen right]

0ms:    Start animation
        
200ms:  Slide in from right
        [opacity: 0→1, x: 50→0]
        
300ms:  Overshoot (spring effect)
        [x: 0→-5]
        
500ms:  Settle
        [x: -5→0, complete]

Result: Smooth spring-based entrance
```

## File Structure

```
frontend/
├── public/
│   ├── favicon.ico
│   └── logo.svg
│
├── src/
│   ├── main.tsx                 ← Entry point
│   ├── App.tsx                  ← Root component
│   ├── index.css                ← Global styles
│   │
│   ├── components/
│   │   ├── ui/                  ← Base components
│   │   │   ├── Button.tsx       ← 4 variants, 3 sizes
│   │   │   ├── Card.tsx         ← + subcomponents
│   │   │   ├── Input.tsx
│   │   │   ├── TextArea.tsx
│   │   │   └── index.ts         ← Barrel export
│   │   │
│   │   ├── layout/              ← Layout components
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Container.tsx
│   │   │
│   │   ├── decision/            ← Feature components
│   │   │   ├── DecisionForm.tsx ← User input form
│   │   │   ├── ProcessGraph.tsx ← Node visualization
│   │   │   ├── NodeCard.tsx     ← Individual node
│   │   │   ├── ProgressBar.tsx  ← Progress indicator
│   │   │   ├── ResultsDisplay.tsx ← Final results
│   │   │   └── StatusIndicator.tsx
│   │   │
│   │   ├── animations/          ← Reusable animations
│   │   │   ├── FadeIn.tsx       ← Fade + slide
│   │   │   ├── SlideIn.tsx      ← Directional slide
│   │   │   ├── Stagger.tsx      ← Staggered children
│   │   │   └── PulseLoader.tsx  ← Loading dots
│   │   │
│   │   ├── ErrorBoundary.tsx    ← Error catcher
│   │   ├── ErrorDisplay.tsx     ← Error UI
│   │   └── LoadingState.tsx     ← Loading UI
│   │
│   ├── hooks/                   ← Custom hooks
│   │   ├── useDecision.ts       ← Context consumer
│   │   ├── useProcessStatus.ts  ← Polling logic
│   │   └── useAnimationSequence.ts
│   │
│   ├── services/                ← API layer
│   │   ├── api.ts               ← Axios instance
│   │   ├── decisionService.ts   ← Decision API
│   │   └── types.ts             ← API types
│   │
│   ├── context/                 ← Global state
│   │   ├── DecisionContext.tsx  ← Main context
│   │   └── ThemeContext.tsx     ← (Optional)
│   │
│   ├── types/                   ← Type definitions
│   │   ├── decision.ts          ← Decision types
│   │   ├── process.ts           ← Process types
│   │   └── graph.ts             ← Graph types
│   │
│   ├── utils/                   ← Utilities
│   │   ├── cn.ts                ← Class merger
│   │   ├── formatters.ts        ← Date, text format
│   │   ├── validators.ts        ← Input validation
│   │   └── constants.ts         ← App constants
│   │
│   └── config/                  ← Configuration
│       ├── env.ts               ← Environment vars
│       └── routes.ts            ← Route definitions
│
├── tests/                       ← Test files
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── .env.example                 ← Env template
├── .env.local                   ← Local env (gitignored)
├── package.json                 ← Dependencies
├── tsconfig.json                ← TypeScript config
├── tailwind.config.js           ← Tailwind config
├── vite.config.ts               ← Vite config
└── README.md                    ← Frontend docs
```

## Technology Stack Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   DEVELOPMENT TOOLS                      │
│  • Vite          - Build tool (fast HMR)                │
│  • TypeScript    - Type safety                          │
│  • ESLint        - Code linting                         │
│  • Prettier      - Code formatting                      │
│  • Vitest        - Unit testing                         │
│  • Playwright    - E2E testing                          │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│                   CORE FRAMEWORK                         │
│  • React 18      - UI library                           │
│  • React Router  - Client-side routing                  │
│  • React Query   - Data fetching & caching              │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│                STYLING & ANIMATIONS                      │
│  • Tailwind CSS  - Utility-first styling                │
│  • Framer Motion - Animation library                    │
│  • Lucide React  - Icon library                         │
│  • Radix UI      - Headless components                  │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│                 DATA & VALIDATION                        │
│  • Axios         - HTTP client                          │
│  • Zod           - Runtime validation                   │
│  • TypeScript    - Compile-time types                   │
└─────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   GITHUB REPOSITORY                      │
│  • Source code                                           │
│  • Version control                                       │
└──────────────────────┬──────────────────────────────────┘
                       │ Push to main
                       ↓
┌─────────────────────────────────────────────────────────┐
│                   GITHUB ACTIONS                         │
│  • Run tests                                             │
│  • Build production bundle                               │
│  • Deploy to Vercel                                      │
└──────────────────────┬──────────────────────────────────┘
                       │ Deploy
                       ↓
┌─────────────────────────────────────────────────────────┐
│                      VERCEL CDN                          │
│  • Global edge network                                   │
│  • Automatic HTTPS                                       │
│  • Instant cache invalidation                            │
└──────────────────────┬──────────────────────────────────┘
                       │ Serve
                       ↓
┌─────────────────────────────────────────────────────────┐
│                        USERS                             │
│  • Fast loading (< 1s)                                   │
│  • Secure connection (HTTPS)                             │
│  • Global availability                                   │
└─────────────────────────────────────────────────────────┘
```

---

*These diagrams provide a visual overview of the frontend architecture. Refer to the detailed documentation for implementation specifics.*
