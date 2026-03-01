"""
Script to fix Colony.gpickle for Python 3 / NetworkX 3.x compatibility
Run this once to convert the old pickle file to a new format
"""
import pickle
import networkx as nx
import numpy as np

print("Attempting to load and fix Colony.gpickle...")

# Try multiple approaches to load the old pickle
try:
    # Attempt 1: Load with latin1 encoding and extract raw data
    with open("Colony.gpickle", 'rb') as f:
        old_data = pickle.load(f, encoding='latin1')
    
    print(f"Loaded object type: {type(old_data)}")
    print(f"Object attributes: {dir(old_data)}")
    
    # Try to extract graph data
    if hasattr(old_data, '__dict__'):
        print(f"Object __dict__: {old_data.__dict__.keys()}")
    
    # Create new graph from scratch
    new_graph = nx.Graph()
    
    # Try to extract nodes - they might be stored differently
    nodes_data = []
    edges_data = []
    
    # Try various attributes where data might be stored
    if hasattr(old_data, 'adj'):
        print("Found adj attribute")
        adj = old_data.adj
        print(f"adj type: {type(adj)}")
    
    if hasattr(old_data, '_adj'):
        print("Found _adj attribute")
        
    if hasattr(old_data, '_node'):
        print("Found _node attribute")
        node_dict = old_data._node
        print(f"_node type: {type(node_dict)}")
        
        # Try to access the actual dict
        if hasattr(node_dict, '_mapping'):
            print("Found _mapping in _node")
            nodes_data = list(node_dict._mapping.keys())
        elif hasattr(node_dict, '__dict__'):
            print("Trying __dict__ on _node")
            
    # Fallback: try to manually extract
    if not nodes_data:
        print("\nTrying manual extraction...")
        print("Attempting to access internal structures...")
        
        # Check if it's really a NetworkX graph
        if isinstance(old_data, nx.Graph):
            print("It reports as NetworkX Graph but internal structure is broken")
            
            # Try the nuclear option: access private attributes directly
            try:
                if hasattr(old_data, '__dict__'):
                    for key, val in old_data.__dict__.items():
                        print(f"  {key}: {type(val)}")
                        if 'node' in key.lower():
                            print(f"    Attempting to extract from {key}")
                            if hasattr(val, '_mapping'):
                                nodes_data = list(val._mapping.keys())
                                print(f"    Found {len(nodes_data)} nodes!")
                                break
            except Exception as e:
                print(f"Error during extraction: {e}")
    
    if nodes_data:
        print(f"\nSuccessfully extracted {len(nodes_data)} nodes")
        new_graph.add_nodes_from(nodes_data)
        
        # Try to get edges
        if hasattr(old_data, '_adj'):
            adj_dict = old_data._adj
            if hasattr(adj_dict, '_mapping'):
                adj_mapping = adj_dict._mapping
                for node, neighbors in adj_mapping.items():
                    if hasattr(neighbors, '_mapping'):
                        for neighbor in neighbors._mapping.keys():
                            edges_data.append((node, neighbor))
                    else:
                        for neighbor in neighbors.keys():
                            edges_data.append((node, neighbor))
        
        if edges_data:
            new_graph.add_edges_from(edges_data)
            print(f"Successfully extracted {len(edges_data)} edges")
        
        # Save the new graph
        with open("Colony_py3.gpickle", 'wb') as f:
            pickle.dump(new_graph, f)
        
        print(f"\n✓ Successfully created Colony_py3.gpickle")
        print(f"  Nodes: {new_graph.number_of_nodes()}")
        print(f"  Edges: {new_graph.number_of_edges()}")
        print("\nRename Colony.gpickle to Colony_old.gpickle")
        print("Then rename Colony_py3.gpickle to Colony.gpickle")
        
    else:
        print("\n✗ Could not extract node data from pickle file")
        print("\nThe Colony.gpickle file may be too corrupted.")
        print("You may need to regenerate it from source data or use a Python 2 environment")
        print("to export it to a compatible format.")

except Exception as e:
    print(f"\n✗ Error loading pickle file: {e}")
    import traceback
    traceback.print_exc()
    
    print("\n\nAlternative: Generate a new colony network")
    print("=" * 60)
    response = input("Generate a new random colony network? (y/n): ")
    
    if response.lower() == 'y':
        # Generate a new colony network
        num_cells = 100
        print(f"Generating new colony with {num_cells} cells...")
        
        # Create cells as nodes
        new_graph = nx.Graph()
        
        # Add nodes with location attributes (simple grid layout)
        np.random.seed(42)
        for i in range(num_cells):
            # Random positions in a roughly circular colony
            angle = np.random.uniform(0, 2 * np.pi)
            radius = np.random.uniform(0, 30) ** 0.5 * 6  # Favor center
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            # Create a simple node object with location
            class CellNode:
                def __init__(self, ID, location):
                    self.ID = ID
                    self.location = np.array([x, y, 0.0])
                    self.state = "U"
                    
            node = CellNode(i, [x, y, 0.0])
            new_graph.add_node(node)
        
        # Add edges based on proximity (cells within 15 um are neighbors)
        nodes = list(new_graph.nodes())
        for i, node1 in enumerate(nodes):
            for node2 in nodes[i+1:]:
                dist = np.linalg.norm(node1.location[:2] - node2.location[:2])
                if dist < 15:
                    new_graph.add_edge(node1, node2)
        
        # Save
        with open("Colony_py3.gpickle", 'wb') as f:
            pickle.dump(new_graph, f)
        
        print(f"\n✓ Generated new colony: Colony_py3.gpickle")
        print(f"  Nodes: {new_graph.number_of_nodes()}")
        print(f"  Edges: {new_graph.number_of_edges()}")
        print("\nRename Colony_py3.gpickle to Colony.gpickle to use it.")
