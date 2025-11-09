# Frontend Architecture Guide: Building a Modern Decision-Making UI

## Table of Contents
1. [Introduction & Overview](#introduction--overview)
2. [Frontend Architecture Decisions](#frontend-architecture-decisions)
3. [Technology Stack Rationale](#technology-stack-rationale)
4. [Application Architecture](#application-architecture)
5. [UI/UX Design Principles](#uiux-design-principles)
6. [Component Architecture](#component-architecture)
7. [State Management Strategy](#state-management-strategy)
8. [Real-Time Updates & Polling](#real-time-updates--polling)
9. [Animation & Visual Feedback](#animation--visual-feedback)
10. [API Integration Patterns](#api-integration-patterns)
11. [Error Handling & Loading States](#error-handling--loading-states)
12. [Performance Optimization](#performance-optimization)
13. [Development Workflow](#development-workflow)
14. [Testing Strategy](#testing-strategy)
15. [Deployment & Production](#deployment--production)

---

## Introduction & Overview

### What We're Building

A **modern, interactive frontend** for the multi-agent decision-making system that:
- Provides a **clean, minimal interface** for decision queries
- **Visualizes the entire decision process** with animated node progression
- Shows **real-time status** of each agent's work
- Displays **comprehensive results** with evaluation feedback
- Offers **responsive design** for desktop and mobile
- Uses **modern animations** for professional feel

### User Experience Flow

```
┌─────────────────────────────────────────────┐
│  1. User enters decision query              │
│     "Should I switch careers?"              │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│  2. Process starts (immediate feedback)     │
│     • Get process ID                         │
│     • Show "Processing..." animation         │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│  3. Real-time progress visualization        │
│     • Animated node graph                    │
│     • Current agent highlighted              │
│     • Status updates as they happen          │
│     • Progress bar/percentage                │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│  4. Results display (expandable sections)   │
│     • Selected decision                      │
│     • Alternative decision                   │
│     • Complete reasoning process             │
│     • Evaluation comments                    │
└─────────────────────────────────────────────┘
```

### Key Requirements

1. **Minimal UI**: Clean, focused interface with no clutter
2. **Modern Design**: Following current design trends (glassmorphism, smooth animations)
3. **Real-Time Feedback**: User sees progress as it happens
4. **Process Visualization**: Show all 10+ agents and their states
5. **Responsive**: Works on desktop, tablet, mobile
6. **Accessible**: WCAG 2.1 Level AA compliance
7. **Fast**: Optimistic UI updates, no unnecessary re-renders

---

## Frontend Architecture Decisions

### Decision 1: Framework Choice

**Options Evaluated:**

| Framework | Pros | Cons | Score |
|-----------|------|------|-------|
| **React** | Huge ecosystem, flexible, great tooling | Requires many decisions, can be complex | 9/10 ⭐ |
| **Vue.js** | Easy to learn, good documentation | Smaller ecosystem than React | 8/10 |
| **Svelte** | Minimal boilerplate, fast | Smaller community, fewer libraries | 7/10 |
| **Next.js** | React + SSR/SSG, great DX | Overkill for SPA, more complex | 8/10 |

**Decision: React 18 with Vite**

**Rationale:**
```
WHY REACT?
✓ Most popular (large community, resources)
✓ Excellent animation libraries (Framer Motion, React Spring)
✓ Great TypeScript support
✓ Hooks API is perfect for our use case
✓ Easy to find developers who know it

WHY VITE?
✓ Lightning-fast development server (hot reload in <50ms)
✓ Modern build tool (ESM-native)
✓ Better than Create React App (which is no longer maintained)
✓ Smaller bundle sizes
✓ Out-of-the-box TypeScript support
```

### Decision 2: Language Choice

**Decision: TypeScript (Strict Mode)**

**Rationale:**
```typescript
// WHY TYPESCRIPT?

// 1. Type Safety: Catch errors at compile time
interface DecisionResponse {
  selected_decision: string;
  alternative_decision: string;
  // TypeScript will error if we misspell or miss a field
}

// 2. Better Autocomplete: IDE knows what properties exist
const result: DecisionResponse = await fetchDecision();
result.selected_decision  // ✓ Autocomplete works!
result.selectd_decision   // ✗ TypeScript error!

// 3. Refactoring Safety: Rename with confidence
// If we rename a type, TypeScript finds all usages

// 4. Documentation: Types are self-documenting
function fetchStatus(processId: string): Promise<ProcessStatus> {
  // No need to guess what this returns!
}

// 5. Integration with Backend: Generate types from OpenAPI spec
// We can auto-generate TypeScript types from your FastAPI backend
```

### Decision 3: Styling Approach

**Options Evaluated:**

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| **CSS Modules** | Scoped styles, no conflicts | Verbose, no design system | ❌ |
| **Styled Components** | CSS-in-JS, dynamic styles | Runtime cost, larger bundle | ❌ |
| **Sass/SCSS** | Powerful preprocessor | Extra build step, verbose | ❌ |
| **Tailwind CSS** | Fast, consistent, minimal bundle | Learning curve, HTML clutter | ✅ **WINNER** |

**Decision: Tailwind CSS 3**

**Rationale:**
```css
/* OLD WAY (CSS Modules or Styled Components): */
.decisionCard {
  background-color: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.decisionCard:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  transform: translateY(-2px);
}

/* TAILWIND WAY: */
<div className="bg-white rounded-lg p-6 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all">

/* WHY TAILWIND?
✓ No context switching (HTML and styles in one place)
✓ Consistent design system (spacing, colors follow a scale)
✓ Purges unused CSS (final bundle only has used classes)
✓ Rapid development (no naming classes)
✓ Easy to make responsive (sm:, md:, lg: prefixes)
✓ No CSS file management
*/
```

### Decision 4: Animation Library

**Decision: Framer Motion**

**Rationale:**
```typescript
// WHY FRAMER MOTION?

// 1. Declarative animations (easy to understand)
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  Content appears smoothly
</motion.div>

// 2. Gesture support (drag, hover, tap)
<motion.div
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
>
  Interactive button
</motion.div>

// 3. Layout animations (automatic!)
<motion.div layout>
  {/* When size changes, animates automatically */}
</motion.div>

// 4. Variants (reusable animation sets)
const variants = {
  hidden: { opacity: 0, x: -100 },
  visible: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 100 }
};

<motion.div
  variants={variants}
  initial="hidden"
  animate="visible"
  exit="exit"
/>

// ALTERNATIVES CONSIDERED:
// - React Spring: More physics-based, higher learning curve
// - CSS Animations: Limited, no gesture support
// - GSAP: Powerful but complex, imperative API
```

### Decision 5: State Management

**Decision: React Context + Custom Hooks (No Redux)**

**Rationale:**
```typescript
// WHY NO REDUX?

// Our state is simple:
// 1. Current query
// 2. Process ID
// 3. Process status
// 4. Results

// For this, Redux is OVERKILL.

// MODERN APPROACH: Context + Hooks
const DecisionContext = createContext<DecisionContextType>(null);

export function DecisionProvider({ children }) {
  const [processId, setProcessId] = useState<string | null>(null);
  const [status, setStatus] = useState<ProcessStatus>('idle');
  const [results, setResults] = useState<DecisionResponse | null>(null);
  
  // Logic here
  
  return (
    <DecisionContext.Provider value={{ processId, status, results, /* ... */ }}>
      {children}
    </DecisionContext.Provider>
  );
}

// Usage in components:
function MyComponent() {
  const { processId, status } = useDecisionContext();
  // Simple, no Redux boilerplate!
}

// WHEN TO USE REDUX?
// - Large apps (100+ components)
// - Complex state updates from many places
// - Need time-travel debugging
// - Team already familiar with it

// OUR CASE: Context is perfect!
```

### Decision 6: API Communication

**Decision: Axios + React Query**

**Rationale:**
```typescript
// WHY AXIOS?
// - Better than fetch() (automatic JSON parsing, interceptors)
// - Error handling is cleaner
// - Request/response interceptors for auth, logging

// WHY REACT QUERY?
// - Automatic caching
// - Automatic refetching
// - Loading and error states built-in
// - No need for useEffect() hell

// EXAMPLE WITHOUT REACT QUERY (complex):
function MyComponent() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    setLoading(true);
    fetchData()
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [/* dependencies? */]);
  
  // Handle loading, error, data...
}

// EXAMPLE WITH REACT QUERY (simple):
function MyComponent() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['status', processId],
    queryFn: () => fetchStatus(processId),
    refetchInterval: 2000  // Auto-poll every 2 seconds!
  });
  
  // That's it!
}
```

---

## Technology Stack Rationale

### Complete Stack

```
┌─────────────────────────────────────────────┐
│         DEVELOPMENT TOOLS                    │
│  • Vite (build tool)                        │
│  • TypeScript (language)                     │
│  • ESLint + Prettier (code quality)         │
│  • Vitest (unit testing)                     │
│  • Playwright (E2E testing)                  │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         FRONTEND FRAMEWORK                   │
│  • React 18 (UI library)                    │
│  • React Router (navigation)                 │
│  • React Query (data fetching)              │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         STYLING & ANIMATIONS                 │
│  • Tailwind CSS (styling)                   │
│  • Framer Motion (animations)               │
│  • Lucide React (icons)                     │
│  • Radix UI (headless components)           │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         API COMMUNICATION                    │
│  • Axios (HTTP client)                      │
│  • React Query (caching/polling)            │
│  • Zod (runtime validation)                 │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         BACKEND API                          │
│  • FastAPI (your existing backend)          │
│  • Redis (persistence)                       │
└─────────────────────────────────────────────┘
```

### Why Each Library?

#### 1. **Radix UI** (Headless UI Components)

```typescript
// WHAT IS RADIX UI?
// Unstyled, accessible components that you style with Tailwind

// WHY?
// ✓ Accessibility built-in (keyboard nav, ARIA attributes)
// ✓ Works with Tailwind (no style conflicts)
// ✓ Handles complex behaviors (dropdowns, modals, tooltips)

// EXAMPLE: Accordion for results
import * as Accordion from '@radix-ui/react-accordion';

<Accordion.Root type="single" collapsible>
  <Accordion.Item value="trigger">
    <Accordion.Trigger className="flex justify-between p-4 hover:bg-gray-50">
      Trigger Analysis
      <ChevronDown />
    </Accordion.Trigger>
    <Accordion.Content className="p-4 text-gray-700">
      {decisionResult.trigger}
    </Accordion.Content>
  </Accordion.Item>
</Accordion.Root>

// ALTERNATIVES:
// - Headless UI (by Tailwind Labs) - also good, slightly different API
// - Material UI - too opinionated, hard to customize
// - Ant Design - same issue
// - Building from scratch - why reinvent the wheel?
```

#### 2. **Lucide React** (Icons)

```typescript
// WHY LUCIDE?
// ✓ Beautiful, consistent icon set
// ✓ Tree-shakeable (only import icons you use)
// ✓ Customizable (size, color, stroke width)
// ✓ Open source

import { Loader2, CheckCircle2, XCircle, Clock } from 'lucide-react';

// EXAMPLE: Status icons
function StatusIcon({ status }) {
  switch (status) {
    case 'running':
      return <Loader2 className="animate-spin text-blue-500" />;
    case 'completed':
      return <CheckCircle2 className="text-green-500" />;
    case 'failed':
      return <XCircle className="text-red-500" />;
    default:
      return <Clock className="text-gray-400" />;
  }
}

// ALTERNATIVES:
// - Heroicons - also good, fewer icons
// - React Icons - huge bundle size
// - Font Awesome - old-school, not React-native
```

#### 3. **Zod** (Runtime Validation)

```typescript
// WHY ZOD?
// TypeScript only validates at compile time.
// Zod validates at runtime (incoming API data).

// EXAMPLE: Validate API response
import { z } from 'zod';

const ProcessStatusSchema = z.object({
  process_id: z.string(),
  status: z.enum(['pending', 'running', 'completed', 'failed']),
  created_at: z.string().optional(),
  result: z.object({
    selected_decision: z.string(),
    // ... more fields
  }).optional()
});

// Use it
async function fetchStatus(processId: string) {
  const response = await axios.get(`/decisions/status/${processId}`);
  
  // Validate and parse (throws error if invalid)
  const data = ProcessStatusSchema.parse(response.data);
  
  // Now TypeScript knows the exact shape!
  return data;
}

// WHY NOT JUST TYPESCRIPT?
// TypeScript: "I trust this is a ProcessStatus" (hope)
// Zod: "I verified this is a ProcessStatus" (proof)
```

---

## Application Architecture

### Folder Structure

```
frontend/
├── public/                      # Static assets
│   ├── favicon.ico
│   └── logo.svg
│
├── src/
│   ├── main.tsx                # Entry point
│   ├── App.tsx                 # Root component
│   ├── index.css               # Global styles (Tailwind imports)
│   │
│   ├── components/             # Reusable UI components
│   │   ├── ui/                 # Base UI components (Button, Card, etc.)
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Input.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── layout/             # Layout components
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Container.tsx
│   │   │
│   │   ├── decision/           # Decision-specific components
│   │   │   ├── DecisionForm.tsx
│   │   │   ├── ProcessGraph.tsx
│   │   │   ├── NodeCard.tsx
│   │   │   ├── ResultsDisplay.tsx
│   │   │   └── StatusIndicator.tsx
│   │   │
│   │   └── animations/         # Animation components
│   │       ├── FadeIn.tsx
│   │       ├── SlideIn.tsx
│   │       └── PulseLoader.tsx
│   │
│   ├── hooks/                  # Custom React hooks
│   │   ├── useDecisionProcess.ts
│   │   ├── useProcessStatus.ts
│   │   ├── useGraphVisualization.ts
│   │   └── useAnimationSequence.ts
│   │
│   ├── services/               # API communication
│   │   ├── api.ts              # Axios instance
│   │   ├── decisionService.ts  # Decision API calls
│   │   └── types.ts            # API type definitions
│   │
│   ├── context/                # React Context
│   │   ├── DecisionContext.tsx
│   │   └── ThemeContext.tsx
│   │
│   ├── utils/                  # Utility functions
│   │   ├── formatters.ts       # Date, text formatting
│   │   ├── validators.ts       # Input validation
│   │   └── constants.ts        # App constants
│   │
│   ├── types/                  # TypeScript type definitions
│   │   ├── decision.ts
│   │   ├── process.ts
│   │   └── graph.ts
│   │
│   └── config/                 # Configuration
│       ├── env.ts              # Environment variables
│       └── routes.ts           # Route definitions
│
├── .env.example                # Environment variables template
├── .eslintrc.json             # ESLint configuration
├── .prettierrc                # Prettier configuration
├── index.html                 # HTML template
├── package.json               # Dependencies
├── tailwind.config.js         # Tailwind configuration
├── tsconfig.json              # TypeScript configuration
├── vite.config.ts             # Vite configuration
└── README.md                  # Frontend documentation
```

### Component Hierarchy

```
App
└── DecisionProvider (Context)
    └── ThemeProvider (Context)
        ├── Header
        │   └── Logo
        │
        └── Container
            └── Main Content
                ├── DecisionForm
                │   ├── Input (query)
                │   ├── Button (submit)
                │   └── ErrorMessage
                │
                ├── ProcessVisualization (conditional)
                │   ├── ProcessGraph
                │   │   ├── NodeCard (for each agent)
                │   │   │   ├── NodeIcon
                │   │   │   ├── NodeTitle
                │   │   │   ├── StatusIndicator
                │   │   │   └── EvaluationBadge
                │   │   │
                │   │   └── ConnectionLines
                │   │
                │   └── ProgressBar
                │
                └── ResultsDisplay (when completed)
                    ├── DecisionCard (selected)
                    │   ├── Title
                    │   ├── Description
                    │   └── Comment
                    │
                    ├── AlternativeCard
                    │   ├── Title
                    │   ├── Description
                    │   └── Comment
                    │
                    └── ProcessDetails (accordion)
                        ├── TriggerSection
                        ├── RootCauseSection
                        ├── ScopeSection
                        ├── GoalsSection
                        └── ... more sections
```

---

## UI/UX Design Principles

### 1. Minimal Design Philosophy

**Inspiration: Linear, Vercel, Stripe**

```css
/* CHARACTERISTICS:
 * 1. Lots of whitespace
 * 2. Subtle borders (gray-200)
 * 3. Limited color palette (mostly neutrals)
 * 4. Accent color for important actions (blue-600)
 * 5. Generous padding (p-6, p-8)
 * 6. Clean typography (Inter or similar)
 */

/* EXAMPLE: Card design */
.card {
  background: white;
  border: 1px solid rgb(229, 231, 235); /* gray-200 */
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); /* very subtle */
}

/* NOT THIS (cluttered): */
.card-bad {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: 3px solid gold;
  border-radius: 25px;
  padding: 10px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.3), 0 0 25px gold;
  /* Too much going on! */
}
```

### 2. Color Palette

```typescript
// PRIMARY COLORS (minimal usage)
const colors = {
  // Brand/Primary (for important actions)
  primary: {
    50: '#eff6ff',   // Very light blue
    100: '#dbeafe',
    500: '#3b82f6',  // Main blue (buttons, links)
    600: '#2563eb',  // Hover state
    700: '#1d4ed8',  // Active state
  },
  
  // Neutrals (main UI)
  gray: {
    50: '#f9fafb',   // Background
    100: '#f3f4f6',  // Secondary background
    200: '#e5e7eb',  // Borders
    400: '#9ca3af',  // Disabled text
    600: '#4b5563',  // Secondary text
    900: '#111827',  // Primary text
  },
  
  // Status colors
  success: '#10b981',  // green-500
  error: '#ef4444',    // red-500
  warning: '#f59e0b',  // amber-500
  info: '#3b82f6',     // blue-500
};

// USAGE RULES:
// - Use gray for 90% of UI
// - Use primary for CTAs (Call To Action buttons)
// - Use status colors only for status indicators
// - No gradients (keep it simple)
```

### 3. Typography Scale

```css
/* DESIGN SYSTEM: */

/* Display (page title) */
.text-display {
  font-size: 2.5rem;     /* 40px */
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

/* Heading 1 (section title) */
.text-h1 {
  font-size: 1.875rem;   /* 30px */
  font-weight: 600;
  line-height: 1.3;
}

/* Heading 2 (subsection) */
.text-h2 {
  font-size: 1.5rem;     /* 24px */
  font-weight: 600;
  line-height: 1.4;
}

/* Heading 3 (card title) */
.text-h3 {
  font-size: 1.125rem;   /* 18px */
  font-weight: 600;
  line-height: 1.4;
}

/* Body (normal text) */
.text-body {
  font-size: 1rem;       /* 16px */
  font-weight: 400;
  line-height: 1.6;
}

/* Small (secondary info) */
.text-small {
  font-size: 0.875rem;   /* 14px */
  font-weight: 400;
  line-height: 1.5;
  color: rgb(107, 114, 128); /* gray-500 */
}

/* Caption (timestamps, metadata) */
.text-caption {
  font-size: 0.75rem;    /* 12px */
  font-weight: 400;
  line-height: 1.4;
  color: rgb(156, 163, 175); /* gray-400 */
}

/* FONT FAMILY:
 * Use Inter (modern, clean, great for UI)
 * Fallback: system fonts
 */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
```

### 4. Spacing System

```typescript
// TAILWIND'S SPACING SCALE (we'll follow this)

const spacing = {
  0: '0px',
  1: '4px',
  2: '8px',
  3: '12px',
  4: '16px',
  5: '20px',
  6: '24px',   // ← Most common padding
  8: '32px',   // ← Large padding
  10: '40px',
  12: '48px',  // ← Section spacing
  16: '64px',  // ← Large section spacing
  20: '80px',
  24: '96px',
};

// USAGE EXAMPLES:

// Small card
<div className="p-4">  {/* 16px padding */}

// Normal card
<div className="p-6">  {/* 24px padding */}

// Large card
<div className="p-8">  {/* 32px padding */}

// Vertical spacing between sections
<div className="space-y-12">  {/* 48px gap */}

// Horizontal spacing between items
<div className="space-x-4">  {/* 16px gap */}
```

### 5. Visual Hierarchy

```
┌────────────────────────────────────────────────┐
│                                                │
│  ┌──────────────────────────────────────────┐ │ ← Level 1: Page title
│  │  Decision Making Assistant               │ │   (large, bold)
│  └──────────────────────────────────────────┘ │
│                                                │
│  ┌──────────────────────────────────────────┐ │ ← Level 2: Section
│  │  What decision do you need help with?    │ │   (medium, semibold)
│  │  ────────────────────────────────        │ │
│  │  [Text input field]                      │ │ ← Level 3: Input
│  │  [Analyze Decision Button]               │ │   (normal size)
│  └──────────────────────────────────────────┘ │
│                                                │
│  ┌──────────────────────────────────────────┐ │ ← Level 2: Results
│  │  Decision Results                        │ │
│  │                                          │ │
│  │  ┌────────────────────────────────────┐ │ │ ← Level 3: Card
│  │  │  Selected Decision                 │ │ │   (card with border)
│  │  │  Should switch careers to PM        │ │ │
│  │  │  ────────────────                  │ │ │
│  │  │  Based on your skills...          │ │ │ ← Level 4: Content
│  │  └────────────────────────────────────┘ │ │   (body text)
│  └──────────────────────────────────────────┘ │
│                                                │
│  Processed in 97s • 10 agents • 9 evaluations │ ← Level 5: Metadata
│                                                │   (small, gray)
└────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Base UI Components

#### Button Component

```typescript
// src/components/ui/Button.tsx

import { ButtonHTMLAttributes, forwardRef } from 'react';
import { Loader2 } from 'lucide-react';
import { cn } from '@/utils/cn';  // Tailwind class merger

type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger';
type ButtonSize = 'sm' | 'md' | 'lg';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const variantStyles: Record<ButtonVariant, string> = {
  primary: 'bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800',
  secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 active:bg-gray-300',
  ghost: 'bg-transparent text-gray-700 hover:bg-gray-100 active:bg-gray-200',
  danger: 'bg-red-600 text-white hover:bg-red-700 active:bg-red-800',
};

const sizeStyles: Record<ButtonSize, string> = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg',
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      children,
      variant = 'primary',
      size = 'md',
      loading = false,
      leftIcon,
      rightIcon,
      className,
      disabled,
      ...props
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        className={cn(
          // Base styles
          'inline-flex items-center justify-center gap-2',
          'font-medium rounded-lg',
          'transition-colors duration-150',
          'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
          'disabled:opacity-50 disabled:cursor-not-allowed',
          // Variant and size
          variantStyles[variant],
          sizeStyles[size],
          className
        )}
        disabled={disabled || loading}
        {...props}
      >
        {loading && <Loader2 className="w-4 h-4 animate-spin" />}
        {!loading && leftIcon}
        {children}
        {!loading && rightIcon}
      </button>
    );
  }
);

Button.displayName = 'Button';

// USAGE:
// <Button>Default</Button>
// <Button variant="secondary" size="lg">Large Secondary</Button>
// <Button loading>Processing...</Button>
// <Button leftIcon={<Plus />}>Add Item</Button>
```

#### Card Component

```typescript
// src/components/ui/Card.tsx

import { HTMLAttributes, forwardRef } from 'react';
import { cn } from '@/utils/cn';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'bordered' | 'elevated';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hoverable?: boolean;
}

const variantStyles = {
  default: 'bg-white border border-gray-200',
  bordered: 'bg-white border-2 border-gray-300',
  elevated: 'bg-white shadow-md',
};

const paddingStyles = {
  none: '',
  sm: 'p-4',
  md: 'p-6',
  lg: 'p-8',
};

export const Card = forwardRef<HTMLDivElement, CardProps>(
  (
    {
      children,
      variant = 'default',
      padding = 'md',
      hoverable = false,
      className,
      ...props
    },
    ref
  ) => {
    return (
      <div
        ref={ref}
        className={cn(
          'rounded-lg',
          variantStyles[variant],
          paddingStyles[padding],
          hoverable && 'transition-shadow duration-200 hover:shadow-lg',
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = 'Card';

// Subcomponents for structured cards
export const CardHeader = ({ children, className, ...props }: HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('mb-4', className)} {...props}>
    {children}
  </div>
);

export const CardTitle = ({ children, className, ...props }: HTMLAttributes<HTMLHeadingElement>) => (
  <h3 className={cn('text-lg font-semibold text-gray-900', className)} {...props}>
    {children}
  </h3>
);

export const CardDescription = ({ children, className, ...props }: HTMLAttributes<HTMLParagraphElement>) => (
  <p className={cn('text-sm text-gray-600 mt-1', className)} {...props}>
    {children}
  </p>
);

export const CardContent = ({ children, className, ...props }: HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('', className)} {...props}>
    {children}
  </div>
);

export const CardFooter = ({ children, className, ...props }: HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('mt-4 pt-4 border-t border-gray-200', className)} {...props}>
    {children}
  </div>
);

// USAGE:
// <Card>
//   <CardHeader>
//     <CardTitle>Decision Results</CardTitle>
//     <CardDescription>Based on your query</CardDescription>
//   </CardHeader>
//   <CardContent>
//     ...content...
//   </CardContent>
//   <CardFooter>
//     <Button>View Details</Button>
//   </CardFooter>
// </Card>
```

### 2. Decision-Specific Components

#### DecisionForm Component

```typescript
// src/components/decision/DecisionForm.tsx

import { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

interface DecisionFormProps {
  onSubmit: (query: string) => void;
  loading?: boolean;
}

export function DecisionForm({ onSubmit, loading = false }: DecisionFormProps) {
  const [query, setQuery] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    if (!query.trim()) {
      setError('Please enter a decision query');
      return;
    }
    
    if (query.length < 10) {
      setError('Please provide more details (at least 10 characters)');
      return;
    }
    
    setError('');
    onSubmit(query);
  };

  return (
    <motion.form
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      onSubmit={handleSubmit}
      className="w-full max-w-2xl mx-auto"
    >
      <div className="space-y-4">
        {/* Title */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-gray-900">
            Decision Assistant
          </h1>
          <p className="text-gray-600">
            Get AI-powered insights for your important decisions
          </p>
        </div>

        {/* Input */}
        <div>
          <label htmlFor="query" className="sr-only">
            Decision Query
          </label>
          <textarea
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="What decision do you need help with? (e.g., Should I switch careers?)"
            rows={4}
            className={cn(
              'w-full px-4 py-3 rounded-lg border',
              'focus:outline-none focus:ring-2 focus:ring-blue-500',
              'placeholder:text-gray-400',
              'transition-colors',
              error ? 'border-red-300' : 'border-gray-300'
            )}
            disabled={loading}
          />
          {error && (
            <p className="mt-2 text-sm text-red-600">{error}</p>
          )}
        </div>

        {/* Submit Button */}
        <Button
          type="submit"
          size="lg"
          className="w-full"
          loading={loading}
          leftIcon={!loading && <Sparkles className="w-5 h-5" />}
        >
          {loading ? 'Analyzing...' : 'Analyze Decision'}
        </Button>

        {/* Helper Text */}
        <p className="text-xs text-center text-gray-500">
          Your decision will be analyzed by 10+ specialized AI agents
        </p>
      </div>
    </motion.form>
  );
}
```

#### NodeCard Component (for process visualization)

```typescript
// src/components/decision/NodeCard.tsx

import { motion } from 'framer-motion';
import { CheckCircle2, Circle, Loader2, XCircle } from 'lucide-react';
import { Card } from '@/components/ui/Card';

type NodeStatus = 'pending' | 'running' | 'completed' | 'failed';

interface NodeCardProps {
  title: string;
  description?: string;
  status: NodeStatus;
  evaluationStatus?: 'correct' | 'incorrect' | null;
  index: number;
}

const statusConfig = {
  pending: {
    icon: Circle,
    color: 'text-gray-400',
    bgColor: 'bg-gray-50',
    borderColor: 'border-gray-200',
  },
  running: {
    icon: Loader2,
    color: 'text-blue-500',
    bgColor: 'bg-blue-50',
    borderColor: 'border-blue-200',
    iconClassName: 'animate-spin',
  },
  completed: {
    icon: CheckCircle2,
    color: 'text-green-500',
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200',
  },
  failed: {
    icon: XCircle,
    color: 'text-red-500',
    bgColor: 'bg-red-50',
    borderColor: 'border-red-200',
  },
};

export function NodeCard({
  title,
  description,
  status,
  evaluationStatus,
  index,
}: NodeCardProps) {
  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1, duration: 0.3 }}
    >
      <Card
        className={cn(
          'transition-all duration-300',
          config.bgColor,
          config.borderColor,
          'border-2'
        )}
        padding="md"
        hoverable={status === 'completed'}
      >
        <div className="flex items-start gap-3">
          {/* Status Icon */}
          <div className="flex-shrink-0 mt-1">
            <Icon
              className={cn(
                'w-5 h-5',
                config.color,
                config.iconClassName
              )}
            />
          </div>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <h4 className="font-semibold text-gray-900">{title}</h4>
            {description && (
              <p className="mt-1 text-sm text-gray-600">{description}</p>
            )}

            {/* Evaluation Badge */}
            {evaluationStatus && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                className="mt-2"
              >
                <span
                  className={cn(
                    'inline-flex items-center gap-1 px-2 py-1 rounded-md text-xs font-medium',
                    evaluationStatus === 'correct'
                      ? 'bg-green-100 text-green-700'
                      : 'bg-amber-100 text-amber-700'
                  )}
                >
                  {evaluationStatus === 'correct' ? '✓' : '⚠'} Evaluated
                </span>
              </motion.div>
            )}
          </div>
        </div>
      </Card>
    </motion.div>
  );
}
```

---

*This document continues with sections on State Management, Real-Time Updates, Animations, API Integration, etc. Would you like me to continue with the remaining sections?*
