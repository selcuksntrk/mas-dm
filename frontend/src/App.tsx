import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import DecisionForm from '@/components/decision/DecisionForm';
import ProcessStatus from '@/components/decision/ProcessStatus';
import ProcessGraph from '@/components/decision/ProcessGraph';
import ResultsDisplay from '@/components/decision/ResultsDisplay';
import { useDecisionStatus, useApiHealth } from '@/hooks/useDecisionProcess';
import { Activity, CheckCircle2, XCircle } from 'lucide-react';

function App() {
  const [currentProcessId, setCurrentProcessId] = useState<string | null>(null);
  const { data: healthData } = useApiHealth();
  const { data: processState, isLoading } = useDecisionStatus(currentProcessId);

  const handleProcessCreated = (processId: string) => {
    setCurrentProcessId(processId);
  };

  const handleReset = () => {
    setCurrentProcessId(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Multi-Agent Decision System
                </h1>
                <p className="text-sm text-gray-600">
                  AI-Powered Decision Making Platform
                </p>
              </div>
            </div>
            
            {/* API Health Status */}
            <div className="flex items-center gap-2">
              {healthData?.status === 'healthy' ? (
                <>
                  <CheckCircle2 className="w-5 h-5 text-green-600" />
                  <span className="text-sm font-medium text-green-600">API Connected</span>
                </>
              ) : (
                <>
                  <XCircle className="w-5 h-5 text-red-600" />
                  <span className="text-sm font-medium text-red-600">API Offline</span>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <AnimatePresence mode="wait">
          {!currentProcessId ? (
            <motion.div
              key="form"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <DecisionForm onProcessCreated={handleProcessCreated} />
            </motion.div>
          ) : (
            <motion.div
              key="results"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="space-y-6"
            >
              {/* Back Button */}
              <button
                onClick={handleReset}
                className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center gap-2"
              >
                ← Submit New Query
              </button>

              {/* Process Status */}
              {isLoading && (
                <div className="text-center py-12">
                  <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                  <p className="mt-4 text-gray-600">Loading process status...</p>
                </div>
              )}

              {processState && (
                <>
                  <ProcessStatus processState={processState} />
                  <ProcessGraph processState={processState} />
                  <ResultsDisplay processState={processState} />
                </>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Footer */}
      <footer className="mt-16 py-8 border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 text-center text-sm text-gray-600">
          <p>Powered by PydanticAI • FastAPI • React • Tailwind CSS</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
