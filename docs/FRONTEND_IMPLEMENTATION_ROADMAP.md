# Frontend Implementation Roadmap

## Overview

This document provides a **step-by-step implementation plan** for building the frontend application. Follow this roadmap to build the application systematically, testing each part before moving to the next.

---

## Phase 1: Project Setup & Foundation (Day 1)

### 1.1 Initialize Project

```bash
# Create React + Vite + TypeScript project
npm create vite@latest frontend -- --template react-ts

cd frontend

# Install dependencies
npm install

# Install core dependencies
npm install react-router-dom axios @tanstack/react-query framer-motion

# Install UI libraries
npm install tailwindcss postcss autoprefixer
npm install lucide-react clsx tailwind-merge
npm install @radix-ui/react-accordion @radix-ui/react-dialog

# Install validation
npm install zod

# Install dev dependencies
npm install -D @types/node
npm install -D prettier eslint-config-prettier
```

### 1.2 Configure Tailwind CSS

```bash
# Initialize Tailwind
npx tailwindcss init -p
```

```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      animation: {
        'spin-slow': 'spin 3s linear infinite',
      },
    },
  },
  plugins: [],
}
```

```css
/* src/index.css */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900 antialiased;
  }
}
```

### 1.3 Setup TypeScript Configuration

```json
// tsconfig.json (add these to compilerOptions)
{
  "compilerOptions": {
    // ... existing options
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
```

### 1.4 Create Folder Structure

```bash
mkdir -p src/{components/{ui,layout,decision,animations},hooks,services,context,types,utils,config}
```

### 1.5 Environment Variables

```bash
# .env.example
VITE_API_BASE_URL=http://localhost:8001
VITE_APP_NAME=Decision Assistant
```

```bash
# .env.local
VITE_API_BASE_URL=http://localhost:8001
```

**✅ Checkpoint:** Run `npm run dev` and verify the app loads

---

## Phase 2: Base UI Components (Day 2)

### 2.1 Create Utility Functions

```typescript
// src/utils/cn.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### 2.2 Build Button Component

Create `src/components/ui/Button.tsx` with:
- Multiple variants (primary, secondary, ghost, danger)
- Multiple sizes (sm, md, lg)
- Loading state
- Icon support

**Test:** Create a simple page with all button variants

### 2.3 Build Card Component

Create `src/components/ui/Card.tsx` with:
- CardHeader, CardTitle, CardDescription
- CardContent, CardFooter
- Different variants

**Test:** Create a page showing different card layouts

### 2.4 Build Input Component

Create `src/components/ui/Input.tsx` and `TextArea.tsx` with:
- Label support
- Error state
- Helper text
- Disabled state

**Test:** Create a form with various inputs

### 2.5 Create Layout Components

```typescript
// src/components/layout/Header.tsx
// src/components/layout/Container.tsx
// src/components/layout/Footer.tsx
```

**✅ Checkpoint:** You should have a styled layout with working UI components

---

## Phase 3: API Integration (Day 3)

### 3.1 Setup API Service

Create `src/services/api.ts` with:
- Axios instance with interceptors
- Request/response logging
- Error handling

### 3.2 Create Type Definitions

```typescript
// src/types/decision.ts
export interface ProcessStartResponse {
  process_id: string;
  status: string;
  message: string;
}

export interface DecisionResponse {
  selected_decision: string;
  selected_decision_comment: string;
  alternative_decision: string;
  alternative_decision_comment: string;
  trigger: string;
  root_cause: string;
  scope_definition: string;
  decision_drafted: string;
  goals: string;
  complementary_info: string;
  decision_draft_updated: string;
  alternatives: string;
}

export interface ProcessStatusResponse {
  process_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  created_at?: string;
  completed_at?: string;
  result?: DecisionResponse;
  error?: string;
}
```

### 3.3 Create Decision Service

Create `src/services/decisionService.ts` with:
- Zod schemas for validation
- API methods (startDecision, getStatus, etc.)

### 3.4 Setup React Query

```typescript
// src/main.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5000,
    },
  },
});

// Wrap app with QueryClientProvider
```

**Test:** Create a test page that calls the health endpoint

**✅ Checkpoint:** Successfully fetch data from backend

---

## Phase 4: State Management (Day 4)

### 4.1 Create Decision Context

Create `src/context/DecisionContext.tsx` with:
- State for processId, status, results
- Actions: startDecision, resetDecision
- React Query integration for polling

### 4.2 Create Custom Hooks

```typescript
// src/hooks/useDecision.ts
export function useDecision() {
  const context = useContext(DecisionContext);
  if (!context) {
    throw new Error('useDecision must be used within DecisionProvider');
  }
  return context;
}
```

### 4.3 Setup App Providers

```typescript
// src/App.tsx
import { DecisionProvider } from './context/DecisionContext';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <DecisionProvider>
        <YourApp />
      </DecisionProvider>
    </QueryClientProvider>
  );
}
```

**Test:** Create a component that uses `useDecision()` hook

**✅ Checkpoint:** State management is working

---

## Phase 5: Core Features - Decision Form (Day 5)

### 5.1 Create DecisionForm Component

Create `src/components/decision/DecisionForm.tsx` with:
- Textarea for query input
- Submit button
- Input validation
- Error display
- Loading state

### 5.2 Connect to Context

```typescript
// In DecisionForm
const { startDecision, isProcessing } = useDecision();

const handleSubmit = async (e: FormEvent) => {
  e.preventDefault();
  await startDecision(query);
};
```

### 5.3 Add Animations

- Fade in animation on mount
- Smooth transitions for errors

**Test:** Submit a decision query and verify it starts a process

**✅ Checkpoint:** Can submit decisions and get process IDs

---

## Phase 6: Process Visualization (Day 6-7)

### 6.1 Create StatusIndicator Component

```typescript
// src/components/decision/StatusIndicator.tsx
// Shows current status with appropriate icon and color
```

### 6.2 Create NodeCard Component

Create `src/components/decision/NodeCard.tsx` with:
- Title and description
- Status icon (pending, running, completed, failed)
- Evaluation badge
- Hover effects

### 6.3 Create ProcessGraph Component

Create `src/components/decision/ProcessGraph.tsx` with:
- List of all nodes (10 decision agents + evaluations)
- Current active node highlighting
- Connection lines between nodes
- Staggered animations

### 6.4 Add Graph Data

```typescript
// src/data/graphNodes.ts
export const GRAPH_NODES = [
  { id: 'identify_trigger', title: 'Identify Trigger', description: '...' },
  { id: 'root_cause', title: 'Root Cause Analysis', description: '...' },
  // ... all 10+ agents
];
```

### 6.5 Map Backend Status to Frontend Nodes

```typescript
// Hook to convert backend state to node states
function useGraphNodes(status: ProcessStatusResponse) {
  // Logic to determine which nodes are active, completed, etc.
}
```

**Test:** Start a decision and watch nodes animate as process runs

**✅ Checkpoint:** Process visualization is working with live updates

---

## Phase 7: Results Display (Day 8)

### 7.1 Create ResultsDisplay Component

Create `src/components/decision/ResultsDisplay.tsx` with:
- Selected decision card (prominent)
- Alternative decision card
- Expandable sections for process details

### 7.2 Create Expandable Sections

Use Radix UI Accordion:

```typescript
<Accordion.Root type="multiple">
  <Accordion.Item value="trigger">
    <Accordion.Trigger>Trigger Analysis</Accordion.Trigger>
    <Accordion.Content>{result.trigger}</Accordion.Content>
  </Accordion.Item>
  {/* More sections */}
</Accordion.Root>
```

### 7.3 Add Result Animations

- Slide in when results appear
- Stagger section animations

**Test:** Complete a decision and verify all results display correctly

**✅ Checkpoint:** Full decision flow works end-to-end

---

## Phase 8: Polish & Animations (Day 9)

### 8.1 Create Animation Components

```typescript
// src/components/animations/FadeIn.tsx
// src/components/animations/SlideIn.tsx
// src/components/animations/Stagger.tsx
```

### 8.2 Add Loading States

```typescript
// src/components/LoadingState.tsx
// Skeleton loaders for different states
```

### 8.3 Add Empty States

```typescript
// src/components/EmptyState.tsx
// Show when no decision has been made yet
```

### 8.4 Add Progress Bar

```typescript
// src/components/decision/ProgressBar.tsx
// Animated progress bar showing completion percentage
```

### 8.5 Polish Transitions

- Page transitions
- Modal animations
- Hover effects
- Focus states

**Test:** Go through entire flow and verify all animations feel smooth

**✅ Checkpoint:** App feels polished and professional

---

## Phase 9: Error Handling & Edge Cases (Day 10)

### 9.1 Add Error Boundary

```typescript
// src/components/ErrorBoundary.tsx
```

### 9.2 Add Error Display Components

```typescript
// src/components/ErrorDisplay.tsx
```

### 9.3 Handle Edge Cases

- Network errors
- Timeout errors
- Invalid responses
- Process not found
- Backend unavailable

### 9.4 Add Retry Logic

- Automatic retry with exponential backoff
- Manual retry button

**Test:** Simulate errors (turn off backend) and verify error handling

**✅ Checkpoint:** App handles errors gracefully

---

## Phase 10: Responsive Design (Day 11)

### 10.1 Mobile Layout

- Stack cards vertically
- Adjust spacing
- Touch-friendly buttons (larger)
- Simplified animations

### 10.2 Tablet Layout

- Two-column layout where appropriate
- Adjusted graph visualization

### 10.3 Desktop Layout

- Full featured layout
- Side-by-side comparisons
- Extended graph view

### 10.4 Test Responsiveness

```css
/* Use Tailwind breakpoints */
<div className="
  grid grid-cols-1 
  md:grid-cols-2 
  lg:grid-cols-3 
  gap-4
">
```

**Test:** Test on mobile (iPhone), tablet (iPad), desktop

**✅ Checkpoint:** App works on all screen sizes

---

## Phase 11: Accessibility (Day 12)

### 11.1 Keyboard Navigation

- Tab order makes sense
- All interactive elements are keyboard accessible
- Focus states are visible

### 11.2 Screen Reader Support

- Proper ARIA labels
- Semantic HTML
- Alt text for icons

### 11.3 Color Contrast

- All text meets WCAG AA standards
- Don't rely solely on color to convey information

### 11.4 Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Test:** Use keyboard only, test with screen reader (NVDA/VoiceOver)

**✅ Checkpoint:** App is accessible

---

## Phase 12: Performance Optimization (Day 13)

### 12.1 Code Splitting

```typescript
// Lazy load routes
const ResultsPage = lazy(() => import('./pages/ResultsPage'));

<Suspense fallback={<LoadingState />}>
  <ResultsPage />
</Suspense>
```

### 12.2 Optimize Bundle Size

```bash
# Analyze bundle
npm run build
npm install -D vite-plugin-bundle-analyzer
```

### 12.3 Memoization

```typescript
// Memoize expensive computations
const processedNodes = useMemo(() => {
  return transformNodes(rawNodes);
}, [rawNodes]);

// Memoize callbacks
const handleSubmit = useCallback(() => {
  // ...
}, [dependencies]);
```

### 12.4 Image Optimization

- Use WebP format
- Lazy load images
- Responsive images

**Test:** Run Lighthouse audit, aim for 90+ score

**✅ Checkpoint:** App is performant

---

## Phase 13: Testing (Day 14-15)

### 13.1 Unit Tests

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

```typescript
// src/components/ui/__tests__/Button.test.tsx
import { render, screen } from '@testing-library/react';
import { Button } from '../Button';

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
  
  it('shows loading state', () => {
    render(<Button loading>Submit</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### 13.2 Integration Tests

Test complete user flows:
- Submit decision → see progress → view results

### 13.3 E2E Tests

```bash
npm install -D @playwright/test
```

```typescript
// tests/decision-flow.spec.ts
import { test, expect } from '@playwright/test';

test('complete decision flow', async ({ page }) => {
  await page.goto('http://localhost:3000');
  
  // Fill form
  await page.fill('textarea', 'Should I switch careers?');
  await page.click('button[type="submit"]');
  
  // Wait for processing
  await page.waitForSelector('[data-testid="process-graph"]');
  
  // Verify results appear
  await page.waitForSelector('[data-testid="results"]', { timeout: 120000 });
  
  expect(await page.textContent('[data-testid="selected-decision"]')).toBeTruthy();
});
```

**✅ Checkpoint:** Core functionality is tested

---

## Phase 14: Documentation (Day 16)

### 14.1 Create README.md

```markdown
# Decision Assistant Frontend

## Getting Started

\`\`\`bash
npm install
npm run dev
\`\`\`

## Environment Variables

...

## Architecture

...
```

### 14.2 Component Documentation

Add JSDoc comments to components:

```typescript
/**
 * Button component with multiple variants and states
 * 
 * @example
 * <Button variant="primary" size="lg">Click me</Button>
 * <Button loading>Processing...</Button>
 */
export function Button({ ... }) {
```

### 14.3 Create Storybook (Optional)

```bash
npx sb init
```

**✅ Checkpoint:** Documentation is complete

---

## Phase 15: Deployment (Day 17)

### 15.1 Build Configuration

```json
// package.json
{
  "scripts": {
    "build": "tsc && vite build",
    "preview": "vite preview"
  }
}
```

### 15.2 Environment-Specific Configs

```bash
# .env.production
VITE_API_BASE_URL=https://api.yourdomain.com
```

### 15.3 Deploy to Vercel

```bash
npm install -g vercel
vercel
```

Or use GitHub Actions:

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: npm install
      - run: npm run build
      - uses: amondnet/vercel-action@v20
```

### 15.4 Setup CDN

- Enable Vercel Edge Network
- Configure caching headers
- Setup custom domain

**✅ Checkpoint:** App is deployed and accessible

---

## Quick Reference: Daily Tasks

| Day | Focus | Key Deliverables |
|-----|-------|------------------|
| 1 | Setup | Project initialized, dependencies installed |
| 2 | UI Components | Button, Card, Input components ready |
| 3 | API | API service, type definitions, React Query setup |
| 4 | State | Context, hooks, state management |
| 5 | Form | Decision form working, can submit queries |
| 6-7 | Visualization | Process graph with live updates |
| 8 | Results | Results display with all sections |
| 9 | Animations | Smooth animations throughout |
| 10 | Error Handling | Graceful error handling |
| 11 | Responsive | Works on all devices |
| 12 | Accessibility | WCAG AA compliant |
| 13 | Performance | Optimized bundle, fast loading |
| 14-15 | Testing | Unit, integration, E2E tests |
| 16 | Documentation | README, component docs |
| 17 | Deployment | Live on production |

---

## Testing Checklist

### Functional Testing

- [ ] Can submit decision query
- [ ] Process starts successfully
- [ ] Status updates in real-time
- [ ] All nodes show correct status
- [ ] Results display when completed
- [ ] Can start new decision after completion
- [ ] Error handling works
- [ ] Can retry failed process

### UI/UX Testing

- [ ] Animations are smooth
- [ ] Loading states are clear
- [ ] Error messages are helpful
- [ ] Design is consistent
- [ ] Typography is readable
- [ ] Colors have good contrast
- [ ] Spacing feels balanced

### Responsive Testing

- [ ] Works on iPhone (375px)
- [ ] Works on iPad (768px)
- [ ] Works on desktop (1440px)
- [ ] Works on large screens (1920px+)
- [ ] Touch targets are large enough
- [ ] Text is readable at all sizes

### Accessibility Testing

- [ ] Can navigate with keyboard only
- [ ] Screen reader announces content correctly
- [ ] Focus states are visible
- [ ] Color contrast meets WCAG AA
- [ ] Reduced motion is respected
- [ ] Forms have proper labels

### Performance Testing

- [ ] Lighthouse score > 90
- [ ] First Contentful Paint < 1.5s
- [ ] Time to Interactive < 3s
- [ ] Bundle size < 500KB
- [ ] No layout shifts
- [ ] Smooth 60fps animations

### Browser Testing

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

---

## Common Issues & Solutions

### Issue: Animations are janky

**Solution:**
- Only animate `transform` and `opacity`
- Use `will-change` CSS property
- Reduce animation complexity
- Check for memory leaks

### Issue: Bundle size is too large

**Solution:**
- Implement code splitting
- Lazy load routes and components
- Tree-shake unused code
- Use lighter alternatives (e.g., date-fns instead of moment)

### Issue: API calls are slow

**Solution:**
- Implement request caching
- Optimize backend responses
- Use compression (gzip/brotli)
- Add loading skeletons for perceived performance

### Issue: TypeScript errors

**Solution:**
- Run `npm run type-check` to find all errors
- Use `any` sparingly (fix type issues properly)
- Generate types from backend OpenAPI spec

### Issue: Tests are failing

**Solution:**
- Check test environment setup
- Mock API calls properly
- Use `act()` for async state updates
- Clean up side effects in tests

---

## Resources

### Official Documentation
- React: https://react.dev
- TypeScript: https://www.typescriptlang.org
- Vite: https://vitejs.dev
- Tailwind CSS: https://tailwindcss.com
- Framer Motion: https://www.framer.com/motion
- React Query: https://tanstack.com/query

### Design Inspiration
- Linear: https://linear.app
- Vercel: https://vercel.com
- Stripe: https://stripe.com
- Raycast: https://raycast.com

### Learning Resources
- React TypeScript Cheatsheet: https://react-typescript-cheatsheet.netlify.app
- Tailwind UI: https://tailwindui.com
- Radix UI: https://www.radix-ui.com

---

## Next Steps After Launch

1. **Analytics Integration**
   - Add Google Analytics or Plausible
   - Track user flows and drop-off points
   - A/B test different UIs

2. **User Feedback**
   - Add feedback widget
   - User interviews
   - Survey important features

3. **Performance Monitoring**
   - Add Sentry for error tracking
   - Monitor Core Web Vitals
   - Set up alerts for issues

4. **Feature Enhancements**
   - Save decision history
   - Export results as PDF
   - Share results via link
   - Compare multiple decisions

5. **Advanced Features**
   - Real-time updates via WebSocket
   - Collaborative decision making
   - Decision templates
   - Integration with other tools

---

**You now have a complete roadmap to build a production-ready frontend! Follow each phase systematically, test thoroughly, and don't skip the polish phases. Good luck! 🚀**
