import { motion } from 'framer-motion';
import Card from '@/components/ui/Card';

export function ProcessGraphSkeleton() {
  return (
    <Card>
      <div className="animate-pulse space-y-6">
        {/* Header */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gray-200 rounded-lg"></div>
          <div className="flex-1">
            <div className="h-6 bg-gray-200 rounded w-48 mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-64"></div>
          </div>
        </div>

        {/* Legend */}
        <div className="h-12 bg-gray-100 rounded-lg"></div>

        {/* Start Node */}
        <div className="flex justify-center">
          <div className="w-48 h-16 bg-gray-200 rounded-lg"></div>
        </div>

        {/* Decision Agents */}
        <div className="grid grid-cols-5 gap-3">
          {Array.from({ length: 10 }).map((_, i) => (
            <div key={i} className="h-20 bg-gray-200 rounded-lg"></div>
          ))}
        </div>

        {/* Aggregate Node */}
        <div className="flex justify-center">
          <div className="w-64 h-16 bg-gray-200 rounded-lg"></div>
        </div>

        {/* Evaluators */}
        <div className="grid grid-cols-3 gap-3">
          {Array.from({ length: 9 }).map((_, i) => (
            <div key={i} className="h-20 bg-gray-200 rounded-lg"></div>
          ))}
        </div>
      </div>
    </Card>
  );
}

export function ResultsSkeleton() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <Card>
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/3"></div>
          <div className="h-20 bg-gray-200 rounded"></div>
          <div className="flex gap-4">
            <div className="h-6 bg-gray-200 rounded w-32"></div>
            <div className="h-6 bg-gray-200 rounded w-32"></div>
          </div>
        </div>
      </Card>

      {Array.from({ length: 3 }).map((_, i) => (
        <Card key={i}>
          <div className="animate-pulse space-y-3">
            <div className="h-6 bg-gray-200 rounded w-48"></div>
            <div className="h-16 bg-gray-100 rounded"></div>
            <div className="h-16 bg-gray-100 rounded"></div>
          </div>
        </Card>
      ))}
    </motion.div>
  );
}
