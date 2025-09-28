# MiniZinc Constraint Solver MCP Server

A Model Context Protocol (MCP) server that provides constraint solving capabilities using MiniZinc. This server allows you to solve various constraint satisfaction and optimization problems through a simple API.

## Features

The server provides the following constraint solving tools:

### Core Tools

1. **solve_constraint** - General purpose constraint solver that accepts any MiniZinc model
2. **validate_model** - Validates MiniZinc model syntax without solving
3. **list_solvers** - Lists all available MiniZinc solvers on the system

### Specialized Problem Solvers

1. **solve_nqueens** - Solves the N-Queens problem
2. **solve_knapsack** - Solves 0/1 knapsack optimization problems
3. **solve_sudoku** - Solves 9×9 Sudoku puzzles
4. **solve_graph_coloring** - Solves graph coloring problems with optional color minimization

## Prerequisites

- Python 3.8 or higher
- MiniZinc 2.6 or higher (must be installed separately)

### Installing MiniZinc

Download and install MiniZinc from: https://www.minizinc.org/software.html

Ensure the `minizinc` executable is in your system PATH.

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd ccake
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

```bash
python main.py
```

The server runs using SSE transport by default.

### Example: Solving N-Queens

To solve the 4-Queens problem and get all solutions:

```python
result = await solve_nqueens(n=4, all_solutions=True)
```

### Example: Custom Constraint Model

You can solve any constraint problem by providing a MiniZinc model:

```python
problem = ConstraintModel(
    model="""
        var 1..10: x;
        var 1..10: y;
        constraint x + y = 15;
        constraint x < y;
        solve satisfy;
    """,
    solver="gecode"
)
result = await solve_constraint(problem)
```

### Example: Knapsack Problem

```python
result = await solve_knapsack(
    weights=[2, 3, 4, 5],
    values=[3, 4, 5, 6],
    capacity=7
)
```

## Response Format

All solving tools return a `SolveResult` object containing:
- `solutions`: List of solutions found
- `status`: Solving status (SATISFIED, OPTIMAL, UNSATISFIABLE, etc.)
- `solve_time`: Time taken to solve
- `num_solutions`: Number of solutions found
- `error`: Error message if solving failed

Each solution contains:
- `variables`: Dictionary of variable names to values
- `objective`: Objective value for optimization problems
- `is_optimal`: Whether the solution is optimal

## Available Solvers

The server supports all MiniZinc-compatible solvers installed on your system. Common ones include:
- Gecode (default)
- Chuffed
- OR-Tools
- CBC

Use `list_solvers()` to see all available solvers on your system.

## Error Handling

The server gracefully handles errors including:
- Invalid MiniZinc syntax
- Unsatisfiable constraints
- Solver timeouts
- Missing solver installations

Errors are returned in the `error` field of the response.

## License

MIT License - see LICENSE file for details.