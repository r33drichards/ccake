# MiniZinc Constraint Solver MCP Server

A Model Context Protocol (MCP) server that provides constraint solving capabilities using MiniZinc. This server exposes a single powerful tool for solving constraint satisfaction and optimization problems.

## Features

The server provides one core tool:

- **solve_constraint** - General purpose constraint solver that accepts any MiniZinc model with optional data parameters, solver selection, and timeout configuration

## Usage Options

### Option 1: Use Hosted Version (Recommended)

The easiest way to get started is using our free hosted version at:
```
https://minizinc-mcp.up.railway.app/sse
```

### Option 2: Self-Host with Docker

Build and run locally:
```bash
git clone <repository-url>
cd ccake
docker build -t minizinc-mcp .
docker run -p 8000:8000 minizinc-mcp
```

### Option 3: Local Development

Prerequisites:
- Python 3.11+
- MiniZinc 2.8+ (install from https://www.minizinc.org/software.html)

```bash
git clone <repository-url>
cd ccake
pip install -r requirements.txt
python main.py
```

# Usage with Claude 

got to the [connectors settings page](https://claude.ai/settings/connectors)

click `Add Custom Connector` button 

for name use "minizinc mcp" 

for url use:
 
    https://minizinc-mcp.up.railway.app/sse

## Example Usage

Once configured, you can ask Claude to solve constraint problems:

*"Solve the 4-Queens problem where 4 queens must be placed on a 4x4 chessboard so that no two queens attack each other"*

*"Find the optimal solution to a knapsack problem with items having weights [2,3,4,5] and values [3,4,5,6] and capacity 7"*

*"Solve this custom constraint: I need two variables x and y between 1 and 10 where x + y = 15 and x < y"*

## Response Format

The solve_constraint tool returns a `SolveResult` object containing:
- `solutions`: List of solutions found
- `status`: Solving status (SATISFIED, OPTIMAL, UNSATISFIABLE, etc.)
- `solve_time`: Time taken to solve in seconds
- `num_solutions`: Number of solutions found
- `error`: Error message if solving failed

Each solution contains:
- `variables`: Dictionary of variable names to values
- `objective`: Objective value for optimization problems
- `is_optimal`: Whether the solution is optimal

## License

MIT License - see LICENSE file for details.