#!/usr/bin/env python3
"""
Simple test to verify MiniZinc Python is working
"""

import minizinc

def test_minizinc():
    """Test that MiniZinc is installed and working"""
    try:
        # Try to get Gecode solver
        solver = minizinc.Solver.lookup("gecode")
        print(f"✓ Found solver: {solver.name} v{solver.version}")

        # Create a simple model
        model = minizinc.Model()
        model.add_string("""
            var 1..10: x;
            var 1..10: y;
            constraint x + y = 10;
            constraint x < y;
            solve satisfy;
        """)
        print("✓ Model created successfully")

        # Create instance and solve
        instance = minizinc.Instance(solver, model)
        result = instance.solve()

        if result.status == minizinc.Status.SATISFIED:
            print(f"✓ Solution found: x={result['x']}, y={result['y']}")
        else:
            print(f"✗ No solution found: {result.status}")

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nMake sure MiniZinc is installed:")
        print("  - Download from: https://www.minizinc.org/software.html")
        print("  - Ensure 'minizinc' is in your PATH")
        return False

if __name__ == "__main__":
    print("Testing MiniZinc Python Installation")
    print("=" * 40)

    if test_minizinc():
        print("\n✅ MiniZinc is properly installed!")
    else:
        print("\n❌ MiniZinc is not properly installed")