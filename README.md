# ccake-mcp

MiniZinc Constraint Solver MCP - Solve constraint satisfaction and optimization problems using MiniZinc

## Description

This MCP server provides an interface to solve constraint satisfaction and optimization problems using the MiniZinc constraint modeling language. It allows Claude and other AI systems to solve complex combinatorial problems by leveraging MiniZinc's powerful constraint solvers.

## Features

- Solve constraint satisfaction problems (CSPs)
- Solve constraint optimization problems (COPs)
- Support for multiple MiniZinc solvers (Gecode, Chuffed, etc.)
- Customizable timeout settings
- Support for finding all solutions or just optimal solutions
- Detailed solution reporting with solve statistics

## Installation

```bash
pip install ccake-mcp
```

## Usage

The server provides tools for solving MiniZinc constraint problems. You can provide MiniZinc models as strings along with data parameters and solver preferences.

## Tools

- `solve_constraint`: Solve constraint satisfaction or optimization problems using MiniZinc
- `list_solvers`: Get information about available MiniZinc solvers

## Requirements

- Python 3.8+
- MiniZinc (automatically installed via the minizinc Python package)

## License

MIT License - see LICENSE file for details.