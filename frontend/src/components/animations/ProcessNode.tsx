import { motion } from 'framer-motion';
import { CheckCircle2, Circle, Loader2, XCircle, Clock } from 'lucide-react';
import type { GraphNode } from '@/types/decision';

interface ProcessNodeProps {
  node: GraphNode;
  index: number;
}

export default function ProcessNode({ node, index }: ProcessNodeProps) {
  const getStatusIcon = () => {
    switch (node.status) {
      case 'pending':
        return <Clock className="w-4 h-4 text-gray-400" />;
      case 'running':
      case 'processing':
        return <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />;
      case 'completed':
        return <CheckCircle2 className="w-4 h-4 text-green-600" />;
      case 'failed':
        return <XCircle className="w-4 h-4 text-red-600" />;
      default:
        return <Circle className="w-4 h-4 text-gray-400" />;
    }
  };

  const getNodeColor = () => {
    switch (node.status) {
      case 'pending':
        return 'bg-gray-100 border-gray-300 text-gray-600';
      case 'running':
      case 'processing':
        return 'bg-blue-50 border-blue-400 text-blue-900 shadow-lg shadow-blue-200';
      case 'completed':
        return 'bg-green-50 border-green-400 text-green-900';
      case 'failed':
        return 'bg-red-50 border-red-400 text-red-900';
      default:
        return 'bg-gray-100 border-gray-300 text-gray-600';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: index * 0.05, duration: 0.3 }}
      className={`relative p-3 rounded-lg border-2 ${getNodeColor()} transition-all duration-300`}
    >
      <div className="flex items-start gap-2">
        <div className="flex-shrink-0 mt-0.5">{getStatusIcon()}</div>
        <div className="flex-1 min-w-0">
          <h4 className="text-xs font-semibold truncate">{node.label}</h4>
        </div>
      </div>
    </motion.div>
  );
}
