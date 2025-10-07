import pytest
from main import ConstraintModel, solve_constraint_core


@pytest.mark.asyncio
async def test_timeout_param_smoke():
    problem = ConstraintModel(
        model="var 1..10: x; solve satisfy;",
        solver="gecode",
        timeout=1,
    )
    res = await solve_constraint_core(problem)
    assert res.status != "ERROR"
    assert res.num_solutions >= 1
