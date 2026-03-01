"""
Script to fix Colony.gpickle - simplified version
"""
import pickle
import networkx as nx

print("Loading Colony_old.gpickle...")

with open("Colony_old.gpickle", 'rb') as f:
    old_graph = pickle.load(f, encoding='latin1')

print(f"Loaded: {type(old_graph)}")

# Access the internal dicts directly
node_dict = old_graph.__dict__['node']
adj_dict = old_graph.__dict__['adj']

print(f"Found {len(node_dict)} nodes")
print(f"Found {len(adj_dict)} adjacency entries")

# Create new graph
new_graph = nx.Graph()

# Add nodes with their attributes
for node, attrs in node_dict.items():
    new_graph.add_node(node, **attrs)
    
print(f"Added {new_graph.number_of_nodes()} nodes to new graph")

# Add edges from adjacency dict
edge_count = 0
seen_edges = set()
for node, neighbors in adj_dict.items():
    for neighbor, edge_attrs in neighbors.items():
        # Use IDs to avoid duplicates (undirected graph)
        edge_id = tuple(sorted([id(node), id(neighbor)]))
        if edge_id not in seen_edges:
            new_graph.add_edge(node, neighbor, **edge_attrs)
            seen_edges.add(edge_id)
            edge_count += 1

print(f"Added {edge_count} edges to new graph")

# Verify nodes have required attributes
sample_nodes = list(new_graph.nodes())[:3]
print(f"\nSample nodes: {sample_nodes}")
for node in sample_nodes:
    print(f"  Node {node}: {type(node)}")
    if hasattr(node, 'location'):
        print(f"    location: {node.location}")
    if hasattr(node, 'ID'):
        print(f"    ID: {node.ID}")

# Save
with open("Colony.gpickle", 'wb') as f:
    pickle.dump(new_graph, f)

print(f"\n✓ Successfully created Colony.gpickle")
print(f"  Nodes: {new_graph.number_of_nodes()}")
print(f"  Edges: {new_graph.number_of_edges()}")
