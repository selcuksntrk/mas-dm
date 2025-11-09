import { motion } from 'framer-motion';
import Card from '@/components/ui/Card';
import ProcessNode from '@/components/animations/ProcessNode';
import { useProcessGraph } from '@/hooks/useProcessGraph';
import { Network } from 'lucide-react';
import type { ProcessState } from '@/types/decision';

interface ProcessGraphProps {
  processState: ProcessState;
}

export default function ProcessGraph({ processState }: ProcessGraphProps) {
  const { nodes } = useProcessGraph(processState);

  // Group nodes by type
  const startNode = nodes.find((n) => n.type === 'start');
  const processNodes = nodes.filter((n) => n.type === 'decision');
  const finalNode = nodes.find((n) => n.type === 'final');

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card>
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-purple-100 rounded-lg">
            <Network className="w-6 h-6 text-purple-600" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Decision Process Flow</h2>
            <p className="text-sm text-gray-600">
              Real-time visualization of the decision-making pipeline
            </p>
          </div>
        </div>

        {/* Legend */}
        <div className="mb-6 p-3 bg-gray-50 rounded-lg">
          <div className="flex flex-wrap gap-4 text-xs">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded-full bg-blue-600"></div>
              <span>Process Step</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded-full bg-green-600"></div>
              <span>Completed</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded-full bg-yellow-600"></div>
              <span>Processing</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded-full bg-gray-400"></div>
              <span>Pending</span>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          {/* Start Node */}
          {startNode && (
            <div className="flex justify-center">
              <div className="w-64">
                <ProcessNode node={startNode} index={0} />
              </div>
            </div>
          )}

          {/* Arrow */}
          <div className="flex justify-center">
            <div className="w-0.5 h-8 bg-gradient-to-b from-gray-300 to-gray-400"></div>
          </div>

          {/* Process Steps Grid */}
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-3 text-center">
              Decision-Making Steps
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
              {processNodes.map((node, index) => (
                <ProcessNode key={node.id} node={node} index={index + 1} />
              ))}
            </div>
          </div>

          {/* Arrow */}
          <div className="flex justify-center">
            <div className="w-0.5 h-8 bg-gradient-to-b from-gray-300 to-gray-400"></div>
          </div>

          {/* Final Node */}
          {finalNode && (
            <div className="flex justify-center">
              <div className="w-64">
                <ProcessNode node={finalNode} index={processNodes.length + 1} />
              </div>
            </div>
          )}
        </div>

        {/* Progress Stats */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-gray-900">
                {nodes.filter((n) => n.status === 'completed').length}
              </div>
              <div className="text-xs text-gray-600">Completed</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-blue-600">
                {nodes.filter((n) => n.status === 'processing').length}
              </div>
              <div className="text-xs text-gray-600">Processing</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-600">
                {nodes.filter((n) => n.status === 'pending').length}
              </div>
              <div className="text-xs text-gray-600">Pending</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-purple-600">
                {Math.round(
                  (nodes.filter((n) => n.status === 'completed').length / nodes.length) * 100
                )}%
              </div>
              <div className="text-xs text-gray-600">Progress</div>
            </div>
          </div>
        </div>
      </Card>
    </motion.div>
  );
}
