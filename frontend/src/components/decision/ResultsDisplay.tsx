import { motion } from 'framer-motion';
import Card from '@/components/ui/Card';
import { Target, FileText, Lightbulb, TrendingUp } from 'lucide-react';
import type { ProcessState } from '@/types/decision';

interface ResultsDisplayProps {
  processState: ProcessState;
}

export default function ResultsDisplay({ processState }: ResultsDisplayProps) {
  if (processState.status !== 'completed' || !processState.result) {
    return null;
  }

  const result = processState.result;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      {/* Final Decision Card */}
      <Card className="bg-gradient-to-br from-green-50 to-blue-50 border-2 border-green-200">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-green-100 rounded-xl">
            <Target className="w-8 h-8 text-green-600" />
          </div>
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Selected Decision</h2>
            <p className="text-lg text-gray-800 leading-relaxed mb-4">
              {result.selected_decision}
            </p>
            {result.selected_decision_comment && (
              <div className="mt-3 p-3 bg-white/50 rounded-lg">
                <p className="text-sm text-gray-700">{result.selected_decision_comment}</p>
              </div>
            )}
          </div>
        </div>
      </Card>

      {/* Alternative Decision */}
      {result.alternative_decision && (
        <Card>
          <div className="flex items-center gap-3 mb-4">
            <Lightbulb className="w-6 h-6 text-yellow-600" />
            <h3 className="text-xl font-bold text-gray-900">Alternative Decision</h3>
          </div>
          <p className="text-gray-800 mb-3">{result.alternative_decision}</p>
          {result.alternative_decision_comment && (
            <div className="p-3 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-700">{result.alternative_decision_comment}</p>
            </div>
          )}
        </Card>
      )}

      {/* Analysis Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Trigger */}
        {result.trigger && (
          <Card>
            <div className="flex items-center gap-2 mb-3">
              <TrendingUp className="w-5 h-5 text-blue-600" />
              <h4 className="font-semibold text-gray-900">Trigger</h4>
            </div>
            <p className="text-sm text-gray-700">{result.trigger}</p>
          </Card>
        )}

        {/* Root Cause */}
        {result.root_cause && (
          <Card>
            <div className="flex items-center gap-2 mb-3">
              <FileText className="w-5 h-5 text-purple-600" />
              <h4 className="font-semibold text-gray-900">Root Cause</h4>
            </div>
            <p className="text-sm text-gray-700">{result.root_cause}</p>
          </Card>
        )}
      </div>

      {/* Detailed Information */}
      {(result.scope_definition || result.goals || result.alternatives) && (
        <Card>
          <h3 className="text-xl font-bold text-gray-900 mb-4">Detailed Analysis</h3>
          
          <div className="space-y-4">
            {result.scope_definition && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Scope Definition</h4>
                <p className="text-sm text-gray-700">{result.scope_definition}</p>
              </div>
            )}

            {result.goals && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Goals</h4>
                <p className="text-sm text-gray-700">{result.goals}</p>
              </div>
            )}

            {result.alternatives && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Alternatives Considered</h4>
                <p className="text-sm text-gray-700">{result.alternatives}</p>
              </div>
            )}

            {result.complementary_info && (
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Additional Information</h4>
                <p className="text-sm text-gray-700">{result.complementary_info}</p>
              </div>
            )}
          </div>
        </Card>
      )}
    </motion.div>
  );
}
