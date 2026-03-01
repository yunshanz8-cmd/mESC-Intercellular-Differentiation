# mESC-Intercellular-Differentiation

An agent-based model of intercellular communication and differentiation within mouse embryonic stem cell populations.

**Quick install:**
```bash
# Install dependencies
pip install -r requirements.txt

# Compile Cython extension
cd mESC_Intercellular_Differentiation_Model
python setup.py build_ext --inplace

# Run simulation
python Model_run.py
```

## Requirements

**Python 3.6 or higher**

### Dependencies
- numpy >= 1.19.0
- scipy >= 1.5.0
- networkx >= 3.0
- matplotlib >= 3.3.0
- scikit-learn >= 0.24.0
- Cython >= 3.0.0

## Installation

### Step 1: Install Python dependencies
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install numpy scipy networkx matplotlib scikit-learn Cython
```

### Step 2: Install C++ Compiler (Windows)

**For Windows users**, you need Microsoft Visual C++ 14.0 or greater to compile the Cython extension:

1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Run the installer and select "Desktop development with C++"
3. Restart your terminal after installation


### Step 3: Compile the Cython extension module
```bash
cd mESC_Intercellular_Differentiation_Model
python setup.py build_ext --inplace
```

## How to Run

### 1. Configure Simulation Parameters

Edit `mESC_Intercellular_Differentiation_Model/Model_initialParameters.py`:
```python
# In the main() function:
ts = 0   # Start time (hours)
te = 72  # End time (hours)
dt = 1   # Time step (hours)
```

Edit `mESC_Intercellular_Differentiation_Model/Model_run.py`:
```python
# Set your output directory (must exist or be creatable)
path = "F:\\yz\\simulations"  # Windows path example
# Or use forward slashes: path = "F:/yz/simulations"

# Number of simulation replicates
length = 1
```

### 2. Run the Simulation
```bash
cd mESC_Intercellular_Differentiation_Model
python Model_run.py
```

### Expected Output

The simulation will:
1. **Create a new numbered folder** in your output directory (e.g., `1.0/`, `2.0/`, etc.)
2. **Generate network snapshots** at each time step (e.g., `network0.0.gpickle`, `network1.0.gpickle`, ..., `network24.0.gpickle`)
3. **Save gradient data** (e.g., `cAMP_0.0`, `cAMP_1.0`, etc.)
4. **Save simulation metadata** (`info.sim` file)
5. **Copy model files** to `copiedTM/` subfolder for reproducibility
6. **Console output** showing:
   - Time progression (0 to 24 hours by default)
   - Number of cell objects at each time step
   - Differentiation events ("diff" or "C Diff" messages)
   - Manual collision detection events

### 3. Visualize Results (Optional)

After simulation completes, generate a visualization:
```bash
python visualize_results.py
```

This will create `visualization.png` showing cell positions and differentiation states at different time points:
- **Blue** = Stem cells (undifferentiated)
- **Orange** = Transitioning cells
- **Red** = Differentiated cells

### 4. Analyze Results (Advanced)

After simulation completes, extract metrics:
```bash
# Edit Compile_sim_metrics.py to set paths
python Compile_sim_metrics.py
```

This generates `sim_pca.npy` containing 7 spatial metrics at each time point.

Run PCA analysis:
```bash
python PCA_analysis.py
```

This visualizes the simulation trajectory in principal component space, showing how the differentiation pattern evolves.

## File Structure After Running

```
simulations/
└── 1.0/                          # First simulation run
    ├── info.sim                  # Simulation metadata
    ├── network0.0.gpickle        # Initial cell network state
    ├── network1.0.gpickle        # State at hour 1
    ├── ...
    ├── network24.0.gpickle       # Final state (24 hours by default)
    ├── cAMP_0.0                  # cAMP gradient data at hour 0
    ├── cAMP_1.0                  # cAMP gradient data at hour 1
    ├── ...
    ├── cAMP_24.0                 # cAMP gradient data at hour 24
    ├── visualization.png         # Cell visualization (if generated)
    ├── sim_pca.npy              # Extracted metrics (after running Compile_sim_metrics.py)
    └── copiedTM/                 # Copy of model code used for this run
```

## Troubleshooting

**Error: "Microsoft Visual C++ 14.0 or greater is required"**
- See Step 2 in Installation section above

**Error: Path does not exist**
- Create the output directory manually before running: `mkdir F:\yz\simulations`

**Error: Cannot find Colony.gpickle**
- Ensure you run from the `mESC_Intercellular_Differentiation_Model` directory
- The `Colony.gpickle` file must be present (contains initial cell positions)

**Error: numpy dtype issues**
- Make sure you have numpy >= 1.19.0 installed
- The code has been updated for modern NumPy versions

**ValueError: Buffer dtype mismatch**
- Recompile the Cython extension: `python setup.py build_ext --inplace`

## Understanding the Simulation

### Cell States
Each cell in the simulation has a `state` attribute:
- **'U'** = Undifferentiated (stem cell)
- **'T'** = Transitioning (just started differentiating)
- **'D'** or other = Differentiated

### Cell Attributes
- **C**: cAMP concentration (continuous value 0.0-1.0)
- **location**: [x, y, z] position in 3D space (micrometers)
- **ID**: Unique cell identifier
- **state**: Differentiation state (see above)
- **division_timer**: Time until next potential cell division

### Simulation Mechanics
1. **Cell Division**: Cells divide based on concentration thresholds and division timers
2. **Differentiation**: Occurs randomly or influenced by intercellular cAMP signaling
3. **Physics**: Cells experience collision detection and spatial arrangement
4. **Signaling**: cAMP diffuses between connected cells via gap junctions

## Python 3 Migration

This project has been migrated from Python 2.7 to Python 3.6+. See [PYTHON3_MIGRATION.md](PYTHON3_MIGRATION.md) for detailed information about the changes made.

### Key Changes
- Updated all print statements to functions
- Fixed NetworkX 3.x compatibility (nodes(), edges(), neighbors() return views)
- Updated NumPy dtypes (np.int → np.int32, np.int_ removed)
- Replaced deprecated pickle functions for NetworkX graphs
- Updated Cython language level to 3
- Fixed exception handling (WindowsError → OSError)
- Reconstructed Colony.gpickle for Python 3/NetworkX 3.x compatibility

## Contributing

When modifying this code:
1. Maintain Python 3.6+ compatibility
2. Test with both NumPy 1.x and 2.x
3. Recompile Cython extensions after modifying `.pyx` files
4. Update `PYTHON3_MIGRATION.md` with significant changes

## License

See original repository for license information.
