"""
Check actual cell states in the simulation
"""
import pickle
import networkx as nx
import sys
sys.path.append('.')
from simulationObjects import StemCell

sim_dir = "F:\\yz\\simulations\\5.0\\"

print("Checking cell states at different time points:")
print("="*60)

for t in [0, 3, 6]:
    with open(f"{sim_dir}network{t}.0.gpickle", "rb") as f:
        net = pickle.load(f)
    
    print(f"\nHour {t}: {len(net.nodes())} cells")
    
    # Check first few nodes to see their attributes
    sample_nodes = list(net.nodes())[:5]
    
    for i, node in enumerate(sample_nodes):
        print(f"  Cell {i}: type={type(node).__name__}")
        
        # Check what attributes exist
        if hasattr(node, 'C'):
            print(f"    C = {node.C}")
        if hasattr(node, 'cellType'):
            print(f"    cellType = {node.cellType}")
        if hasattr(node, 'cell_type'):
            print(f"    cell_type = {node.cell_type}")
        if hasattr(node, 'ID'):
            print(f"    ID = {node.ID}")
        if hasattr(node, 'location'):
            print(f"    location = {node.location[:2]}")  # First 2 coords
    
    # Count unique C values
    c_values = [node.C for node in net.nodes()]
    unique_c = set(c_values)
    print(f"\n  Unique C values: {sorted(unique_c)}")
    for val in sorted(unique_c):
        count = sum(1 for c in c_values if c == val)
        print(f"    C={val}: {count} cells")

print("\n" + "="*60)
