import { useState } from 'react';
import { motion } from 'framer-motion';
import Button from '@/components/ui/Button';
import Card from '@/components/ui/Card';
import Textarea from '@/components/ui/Textarea';
import { useCreateDecision } from '@/hooks/useDecisionProcess';
import { Sparkles } from 'lucide-react';

interface DecisionFormProps {
  onProcessCreated: (processId: string) => void;
}

export default function DecisionForm({ onProcessCreated }: DecisionFormProps) {
  const [query, setQuery] = useState('');
  const createDecision = useCreateDecision();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) return;

    try {
      const response = await createDecision.mutateAsync({ 
        decision_query: query.trim()  // Backend expects 'decision_query'
      });
      onProcessCreated(response.process_id);
      setQuery(''); // Clear form after submission
    } catch (error) {
      console.error('Failed to create decision:', error);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card>
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-blue-100 rounded-lg">
            <Sparkles className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Submit Your Query</h2>
            <p className="text-sm text-gray-600">
              Get comprehensive decision analysis powered by AI
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              What decision do you need help with?
            </label>
            <Textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Example: Should I invest in renewable energy stocks this quarter?"
              rows={6}
              disabled={createDecision.isPending}
              className="text-base"
            />
            <p className="mt-2 text-sm text-gray-500">
              {query.length}/1000 characters
            </p>
          </div>

          {createDecision.isError && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="p-4 bg-red-50 border border-red-200 rounded-lg"
            >
              <p className="text-sm text-red-600">
                Failed to submit query. Please check your connection and try again.
              </p>
            </motion.div>
          )}

          <Button
            type="submit"
            variant="primary"
            size="lg"
            isLoading={createDecision.isPending}
            disabled={!query.trim() || createDecision.isPending || query.length > 1000}
            className="w-full"
          >
            {createDecision.isPending ? 'Submitting...' : 'Start Decision Process'}
          </Button>
        </form>

        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="grid grid-cols-2 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-blue-600">7</div>
              <div className="text-xs text-gray-600">Process Steps</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-purple-600">~15s</div>
              <div className="text-xs text-gray-600">Avg Response Time</div>
            </div>
          </div>
        </div>
      </Card>
    </motion.div>
  );
}
