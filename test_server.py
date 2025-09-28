#!/usr/bin/env python3
"""
Test script for the MiniZinc Constraint Solver MCP Server
"""

import asyncio
from main import create_server, ConstraintModel

async def test_basic_constraint():
    """Test basic constraint solving"""
    print("Testing basic constraint solving...")

    # Import the actual functions
    from main import solve_constraint

    problem = ConstraintModel(
        model="""
        var 1..10: x;
        var 1..10: y;
        constraint x + y = 10;
        constraint x < y;
        solve satisfy;
        """,
        solver="gecode",
        all_solutions=True
    )

    result = await solve_constraint(problem)
    print(f"Status: {result.status}")
    print(f"Solutions found: {result.num_solutions}")
    for i, sol in enumerate(result.solutions):
        print(f"  Solution {i+1}: {sol.variables}")
    print()

async def test_nqueens():
    """Test N-Queens solver"""
    print("Testing N-Queens solver...")

    server = create_server()

    result = await server.solve_nqueens(n=4, all_solutions=True)
    print(f"Status: {result.status}")
    print(f"Solutions found: {result.num_solutions}")
    for i, sol in enumerate(result.solutions):
        print(f"  Solution {i+1}: queens = {sol.variables.get('queens', [])}")
    print()

async def test_knapsack():
    """Test Knapsack solver"""
    print("Testing Knapsack solver...")

    server = create_server()

    result = await server.solve_knapsack(
        weights=[2, 3, 4, 5],
        values=[3, 4, 5, 6],
        capacity=7
    )
    print(f"Status: {result.status}")
    if result.solutions:
        sol = result.solutions[0]
        print(f"Optimal solution: take = {sol.variables.get('take', [])}")
        print(f"Total value: {sol.variables.get('total_value', 0)}")
        print(f"Is optimal: {sol.is_optimal}")
    print()

async def test_model_validation():
    """Test model validation"""
    print("Testing model validation...")

    server = create_server()

    # Valid model
    valid_result = await server.validate_model("""
        var 1..10: x;
        solve satisfy;
    """)
    print(f"Valid model: {valid_result['valid']}")

    # Invalid model
    invalid_result = await server.validate_model("""
        var 1..10: x
        solve satisfy  # Missing semicolon
    """)
    print(f"Invalid model: {invalid_result['valid']}")
    if not invalid_result['valid']:
        print(f"Error: {invalid_result['error']}")
    print()

async def test_solver_list():
    """Test listing available solvers"""
    print("Testing solver listing...")

    server = create_server()

    solvers = await server.list_solvers()
    print(f"Available solvers: {len(solvers)}")
    for solver in solvers:
        print(f"  - {solver.name} ({solver.id}) v{solver.version}")
    print()

async def main():
    """Run all tests"""
    print("=" * 50)
    print("MiniZinc Constraint Solver MCP Server Tests")
    print("=" * 50)
    print()

    # Note: Some tests may fail if MiniZinc is not installed
    try:
        await test_basic_constraint()
    except Exception as e:
        print(f"Basic constraint test failed: {e}\n")

    try:
        await test_nqueens()
    except Exception as e:
        print(f"N-Queens test failed: {e}\n")

    try:
        await test_knapsack()
    except Exception as e:
        print(f"Knapsack test failed: {e}\n")

    try:
        await test_model_validation()
    except Exception as e:
        print(f"Model validation test failed: {e}\n")

    try:
        await test_solver_list()
    except Exception as e:
        print(f"Solver listing test failed: {e}\n")

    print("=" * 50)
    print("Tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())