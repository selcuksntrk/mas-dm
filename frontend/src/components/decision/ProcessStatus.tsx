import { motion } from 'framer-motion';
import Card from '@/components/ui/Card';
import { CheckCircle2, Loader2, XCircle, AlertCircle } from 'lucide-react';
import type { ProcessState } from '@/types/decision';

interface ProcessStatusProps {
  processState: ProcessState;
}

export default function ProcessStatus({ processState }: ProcessStatusProps) {
  const getStatusIcon = () => {
    switch (processState.status) {
      case 'pending':
        return <AlertCircle className="w-8 h-8 text-yellow-600" />;
      case 'running':
      case 'processing':
        return <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />;
      case 'completed':
        return <CheckCircle2 className="w-8 h-8 text-green-600" />;
      case 'failed':
        return <XCircle className="w-8 h-8 text-red-600" />;
      default:
        return <AlertCircle className="w-8 h-8 text-gray-600" />;
    }
  };

  const getStatusColor = () => {
    switch (processState.status) {
      case 'pending':
        return 'bg-yellow-50 border-yellow-200';
      case 'running':
      case 'processing':
        return 'bg-blue-50 border-blue-200';
      case 'completed':
        return 'bg-green-50 border-green-200';
      case 'failed':
        return 'bg-red-50 border-red-200';
      default:
        return 'bg-gray-50 border-gray-200';
    }
  };

  const getStatusText = () => {
    switch (processState.status) {
      case 'pending':
        return 'Process is starting...';
      case 'running':
      case 'processing':
        return 'Processing decision...';
      case 'completed':
        return 'Decision completed successfully!';
      case 'failed':
        return 'Process failed';
      default:
        return 'Unknown status';
    }
  };

  const getExecutionTime = () => {
    const start = new Date(processState.created_at);
    const end = processState.completed_at ? new Date(processState.completed_at) : new Date();
    return ((end.getTime() - start.getTime()) / 1000).toFixed(1);
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      <Card className={`${getStatusColor()} border-2`}>
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0">{getStatusIcon()}</div>
          
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-lg font-semibold text-gray-900">
                {getStatusText()}
              </h3>
              <span className="text-xs font-medium text-gray-500">
                ID: {processState.process_id.slice(0, 8)}
              </span>
            </div>

            <div className="space-y-2">
              <div className="text-sm text-gray-600">
                <span className="font-medium">Started:</span>{' '}
                {new Date(processState.created_at).toLocaleTimeString()}
              </div>

              {processState.completed_at && (
                <div className="text-sm text-gray-600">
                  <span className="font-medium">Completed:</span>{' '}
                  {new Date(processState.completed_at).toLocaleTimeString()}
                </div>
              )}

              <div className="text-sm text-gray-600">
                <span className="font-medium">Execution Time:</span>{' '}
                {getExecutionTime()}s
              </div>

              {processState.error && (
                <div className="mt-2 p-2 bg-red-100 border border-red-300 rounded text-sm text-red-700">
                  <span className="font-medium">Error:</span> {processState.error}
                </div>
              )}
            </div>
          </div>
        </div>
      </Card>
    </motion.div>
  );
}
