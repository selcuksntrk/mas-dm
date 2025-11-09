# Frontend Quick Start Guide

> **Goal:** Get you coding in 30 minutes! 🚀

## Prerequisites Check ✓

```bash
# Check Node.js version (need 18+)
node --version
# Should show: v18.x.x or v20.x.x

# Check npm version
npm --version
# Should show: 9.x.x or 10.x.x

# Verify backend is running
curl http://localhost:8001/health
# Should return: {"status": "healthy", ...}
```

If any of these fail, install:
- Node.js: https://nodejs.org/ (download LTS version)
- Backend: See `/backend/README.md`

---

## Step 1: Create Project (5 minutes)

```bash
# Navigate to project root
cd PydanticAI_v2

# Create React app with TypeScript
npm create vite@latest frontend -- --template react-ts

# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

**Checkpoint:** Run `npm run dev` and see the default Vite + React page at `http://localhost:5173`

---

## Step 2: Install Dependencies (5 minutes)

```bash
# Core dependencies
npm install react-router-dom axios @tanstack/react-query framer-motion

# UI libraries
npm install tailwindcss postcss autoprefixer
npm install lucide-react clsx tailwind-merge
npm install @radix-ui/react-accordion @radix-ui/react-dialog

# Validation
npm install zod

# Dev dependencies
npm install -D @types/node prettier eslint-config-prettier
```

**Checkpoint:** Check `package.json` - you should see all these packages listed

---

## Step 3: Configure Tailwind (5 minutes)

```bash
# Initialize Tailwind
npx tailwindcss init -p
```

**Edit `tailwind.config.js`:**
```javascript
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
    },
  },
  plugins: [],
}
```

**Replace `src/index.css` content:**
```css
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

**Checkpoint:** Run `npm run dev` - page should now have Inter font and gray background

---

## Step 4: Configure TypeScript & Vite (5 minutes)

**Edit `tsconfig.json` - add to `compilerOptions`:**
```json
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

**Edit `vite.config.ts`:**
```typescript
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

**Checkpoint:** Imports like `import { x } from '@/utils'` should now work without errors

---

## Step 5: Create Project Structure (5 minutes)

```bash
# Create all necessary directories
mkdir -p src/components/{ui,layout,decision,animations}
mkdir -p src/{hooks,services,context,types,utils,config}

# Create placeholder files
touch src/components/ui/index.ts
touch src/services/api.ts
touch src/utils/cn.ts
```

**Create `.env.example`:**
```bash
VITE_API_BASE_URL=http://localhost:8001
VITE_APP_NAME=Decision Assistant
```

**Create `.env.local` (copy from example):**
```bash
cp .env.example .env.local
```

**Checkpoint:** Your `src/` folder should have the correct structure

---

## Step 6: First Utility Function (5 minutes)

**Create `src/utils/cn.ts`:**
```typescript
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

**Why?** This utility merges Tailwind classes properly, handling conflicts

**Checkpoint:** No errors when importing: `import { cn } from '@/utils/cn'`

---

## Step 7: First Component - Button (5 minutes)

**Create `src/components/ui/Button.tsx`:**
```typescript
import { ButtonHTMLAttributes, forwardRef } from 'react';
import { cn } from '@/utils/cn';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ children, variant = 'primary', loading, className, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          'px-4 py-2 rounded-lg font-medium transition-colors',
          'focus:outline-none focus:ring-2 focus:ring-blue-500',
          'disabled:opacity-50 disabled:cursor-not-allowed',
          variant === 'primary' && 'bg-blue-600 text-white hover:bg-blue-700',
          variant === 'secondary' && 'bg-gray-200 text-gray-900 hover:bg-gray-300',
          className
        )}
        disabled={disabled || loading}
        {...props}
      >
        {loading ? 'Loading...' : children}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

**Test it in `src/App.tsx`:**
```typescript
import { Button } from './components/ui/Button'

function App() {
  return (
    <div className="min-h-screen flex items-center justify-center gap-4">
      <Button>Primary Button</Button>
      <Button variant="secondary">Secondary Button</Button>
      <Button loading>Loading Button</Button>
    </div>
  )
}

export default App
```

**Checkpoint:** Visit http://localhost:3000 and see three styled buttons

---

## Next Steps

### You're now ready to build! Choose your path:

**Option A: Follow the Detailed Roadmap**
→ Open `docs/FRONTEND_IMPLEMENTATION_ROADMAP.md`
→ Continue from Phase 2

**Option B: Build Core Features First**
→ Create API service (`src/services/decisionService.ts`)
→ Set up React Query
→ Build DecisionForm component
→ Test submitting a query

**Option C: Read Architecture First**
→ Read `docs/FRONTEND_SUMMARY.md`
→ Understand all decisions
→ Then build systematically

---

## Quick Test: Submit Your First Query

**Create `src/services/api.ts`:**
```typescript
import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001',
  timeout: 120000,
});

export async function startDecision(query: string) {
  const response = await api.post('/decisions/start', {
    decision_query: query
  });
  return response.data;
}
```

**Update `src/App.tsx` to test:**
```typescript
import { useState } from 'react';
import { Button } from './components/ui/Button';
import { startDecision } from './services/api';

function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const data = await startDecision(query);
      setResult(data);
      alert(`Success! Process ID: ${data.process_id}`);
    } catch (error) {
      alert('Error: ' + error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <div className="w-full max-w-md space-y-4">
        <h1 className="text-2xl font-bold text-center">
          Decision Assistant
        </h1>
        
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your decision query..."
          rows={4}
          className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        
        <Button 
          onClick={handleSubmit}
          loading={loading}
          className="w-full"
        >
          Start Decision
        </Button>

        {result && (
          <div className="mt-4 p-4 bg-green-50 rounded-lg">
            <p className="text-sm text-green-800">
              Process started! ID: {result.process_id}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
```

**Test:**
1. Run `npm run dev`
2. Visit http://localhost:3000
3. Enter a query: "Should I learn React?"
4. Click "Start Decision"
5. You should see an alert with a process ID!

**Congratulations! 🎉** You've successfully connected your frontend to the backend!

---

## Common Issues & Quick Fixes

### Issue: "Cannot find module '@/utils/cn'"
**Fix:** Restart dev server (`Ctrl+C`, then `npm run dev`)

### Issue: Tailwind styles not working
**Fix:** 
1. Check `tailwind.config.js` has correct content paths
2. Restart dev server

### Issue: CORS error when calling API
**Fix:** Backend should already have CORS enabled. If not, add to `backend/app/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: TypeScript errors
**Fix:** 
1. Install missing types: `npm install -D @types/node`
2. Restart TypeScript server in VS Code: `Cmd+Shift+P` → "Restart TS Server"

---

## Development Workflow

```bash
# Terminal 1: Backend
cd backend
uv run uvicorn app.main:app --port 8001 --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Your app: http://localhost:3000
# Backend API: http://localhost:8001
```

---

## VS Code Extensions (Recommended)

- **ES7+ React/Redux/React-Native snippets** - Code snippets
- **Tailwind CSS IntelliSense** - Autocomplete for Tailwind
- **Prettier** - Code formatting
- **ESLint** - Code linting
- **Error Lens** - Inline error display

---

## Useful Commands

```bash
# Development
npm run dev          # Start dev server

# Build
npm run build       # Production build
npm run preview     # Preview production build

# Code Quality
npm run lint        # Run ESLint
npm run format      # Format with Prettier

# Testing (after setup)
npm run test        # Run tests
npm run test:e2e    # Run E2E tests
```

---

## What to Build Next

### Phase 1: Core Components (Day 1-2)
- [ ] Card component
- [ ] Input component
- [ ] Layout components (Header, Container)

### Phase 2: API Integration (Day 3)
- [ ] Complete API service with Zod validation
- [ ] Set up React Query
- [ ] Create type definitions

### Phase 3: Decision Flow (Day 4-5)
- [ ] DecisionForm with validation
- [ ] Context for state management
- [ ] Connect form to API

### Phase 4: Visualization (Day 6-8)
- [ ] ProcessGraph component
- [ ] NodeCard with animations
- [ ] Real-time polling
- [ ] ResultsDisplay

---

## Resources

### Quick Reference
- [React Docs](https://react.dev)
- [Tailwind Docs](https://tailwindcss.com)
- [TypeScript Handbook](https://typescriptlang.org/docs)

### Your Documentation
- `docs/FRONTEND_SUMMARY.md` - Overview
- `docs/FRONTEND_ARCHITECTURE.md` - Detailed architecture
- `docs/FRONTEND_IMPLEMENTATION_ROADMAP.md` - Step-by-step guide
- `docs/FRONTEND_DIAGRAMS.md` - Visual diagrams

---

## Need Help?

1. **Check the docs** - Most questions are answered there
2. **Review examples** - All components have code examples
3. **Check console** - Browser DevTools shows errors
4. **Read error messages** - TypeScript errors are descriptive

---

## Success Criteria

You're ready to move to the next phase when:

- [x] Project runs without errors
- [x] Can submit a query to backend
- [x] Receive a process ID back
- [x] Button component works with Tailwind styles
- [x] TypeScript autocomplete works
- [x] Hot reload works (changes update instantly)

---

**You're all set! Start building your amazing frontend! 🚀**

Remember:
- Build incrementally (one component at a time)
- Test each part before moving on
- Refer to documentation when stuck
- Have fun! 🎉

---

*Last updated: November 9, 2025*
