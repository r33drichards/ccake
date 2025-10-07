import asyncio
import minizinc
import pytest
from main import ConstraintModel, solve_constraint_core


@pytest.mark.asyncio
async def test_basic_constraint_satisfy():
    problem = ConstraintModel(
        model="""
        var 1..10: x;
        var 1..10: y;
        constraint x + y = 10;
        constraint x < y;
        solve satisfy;
        """,
        solver="gecode",
        all_solutions=False,
    )

    result = await solve_constraint_core(problem)
    assert result.status.endswith("SATISFIED")
    assert result.num_solutions == 1
    sol = result.solutions[0]
    assert 1 <= sol.variables["x"] <= 10
    assert 1 <= sol.variables["y"] <= 10
    assert sol.variables["x"] + sol.variables["y"] == 10
    assert sol.variables["x"] < sol.variables["y"]


@pytest.mark.asyncio
async def test_nqueens_all_solutions_n4():
    model = """
    int: n = 4;
    array[1..n] of var 1..n: queens;
    include "alldifferent.mzn";
    constraint alldifferent(queens);
    constraint alldifferent([ queens[i] + i | i in 1..n ]);
    constraint alldifferent([ queens[i] - i | i in 1..n ]);
    solve satisfy;
    """

    problem = ConstraintModel(
        model=model,
        solver="gecode",
        all_solutions=True,
    )

    result = await solve_constraint_core(problem)
    assert result.status.endswith("ALL_SOLUTIONS") or result.status.endswith("SATISFIED")
    assert result.num_solutions >= 2  # There are 2 solutions for 4-queens


@pytest.mark.asyncio
async def test_knapsack_optimize():
    # Simple 0/1 knapsack: choose subset to maximize total value under capacity
    model = """
    int: n = 4;
    set of int: ITEMS = 1..n;
    array[ITEMS] of int: weights = [2,3,4,5];
    array[ITEMS] of int: values = [3,4,5,6];
    int: capacity = 7;
    array[ITEMS] of var 0..1: take;
    var int: total_weight = sum(i in ITEMS)(weights[i] * take[i]);
    var int: total_value = sum(i in ITEMS)(values[i] * take[i]);
    constraint total_weight <= capacity;
    solve maximize total_value;
    """

    problem = ConstraintModel(
        model=model,
        solver="gecode",
        all_solutions=False,
    )

    result = await solve_constraint_core(problem)
    assert result.status.endswith("OPTIMAL_SOLUTION") or result.status.endswith("SATISFIED")
    assert result.num_solutions == 1
    sol = result.solutions[0]
    # Optimal value expected 9 (e.g., items [2,3] or [1,4])
    total_value = sol.variables.get("total_value")
    objective = sol.variables.get("objective") or getattr(sol, "objective", None)
    assert (total_value == 9) or (objective == 9)
