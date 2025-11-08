"""Debug script to test graph structure function"""

from backend.app.core.graph.executor import decision_graph, get_graph_structure

print("Testing graph structure function...")
print(f"Graph nodes type: {type(decision_graph.nodes)}")
print(f"Number of nodes: {len(decision_graph.nodes)}")
print(f"First node: {decision_graph.nodes[0]}")
print(f"First node type: {type(decision_graph.nodes[0])}")

# Try to get structure
try:
    structure = get_graph_structure()
    print("\n✅ Success!")
    print(f"Total nodes: {structure['total_nodes']}")
    print(f"Agent nodes: {structure['agent_nodes']}")
    print(f"Evaluator nodes: {structure['evaluator_nodes']}")
    print(f"\nFirst 5 nodes:")
    for node in structure['nodes'][:5]:
        print(f"  - {node['name']} ({node['type']})")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
