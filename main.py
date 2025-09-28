from pathlib import Path
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import minizinc
import tempfile
import json

class ConstraintModel(BaseModel):
    """Model for constraint problem definition"""
    model: str  # MiniZinc model as string
    data: Optional[Dict[str, Any]] = None  # Data parameters
    solver: str = "gecode"  # Default solver
    all_solutions: bool = False
    timeout: Optional[int] = None  # Timeout in seconds

class Solution(BaseModel):
    """Model for a single solution"""
    variables: Dict[str, Any]
    objective: Optional[float] = None
    is_optimal: bool = False

class SolveResult(BaseModel):
    """Model for solving results"""
    solutions: List[Solution]
    status: str  # SATISFIED, OPTIMAL, UNSATISFIABLE, etc.
    solve_time: float
    num_solutions: int
    error: Optional[str] = None

class SolverInfo(BaseModel):
    """Model for solver information"""
    id: str
    name: str
    version: str
    tags: List[str]

def create_server():
    mcp = FastMCP(
        name="MiniZinc Constraint Solver MCP",
        instructions="Solve constraint satisfaction and optimization problems using MiniZinc"
    )

    @mcp.tool()
    async def solve_constraint(problem: ConstraintModel) -> SolveResult:
        """
        Solve a constraint satisfaction or optimization problem.

        Provide a MiniZinc model as a string, optional data parameters,
        and solver preferences. Returns solutions found.

        Example model:
        ```
        int: n = 4;
        array[1..n] of var 1..n: queens;
        constraint alldifferent(queens);
        constraint alldifferent(i in 1..n)(queens[i] + i);
        constraint alldifferent(i in 1..n)(queens[i] - i);
        solve satisfy;
        ```
        """
        try:
            # Look up the solver
            solver = minizinc.Solver.lookup(problem.solver)

            # Create a model from the string
            model = minizinc.Model()
            model.add_string(problem.model)

            # Create an instance
            instance = minizinc.Instance(solver, model)

            # Add data parameters if provided
            if problem.data:
                for key, value in problem.data.items():
                    instance[key] = value

            # Solve the problem
            if problem.timeout:
                result = await instance.solve_async(
                    all_solutions=problem.all_solutions,
                    timeout=minizinc.timedelta(seconds=problem.timeout)
                )
            else:
                result = await instance.solve_async(all_solutions=problem.all_solutions)

            # Process the results
            solutions = []

            if result.status == minizinc.Status.SATISFIED or result.status == minizinc.Status.ALL_SOLUTIONS:
                if problem.all_solutions and result:
                    # When all_solutions is True, result is iterable
                    for sol in result:
                        sol_dict = {}
                        for key in sol.__dict__:
                            if not key.startswith('_'):
                                sol_dict[key] = sol.__dict__[key]
                        solutions.append(Solution(
                            variables=sol_dict,
                            objective=sol.objective if hasattr(sol, 'objective') else None,
                            is_optimal=False
                        ))
                elif result.solution:
                    # Single solution case
                    sol_dict = {}
                    for key in result.solution.__dict__:
                        if not key.startswith('_'):
                            sol_dict[key] = result.solution.__dict__[key]
                    solutions.append(Solution(
                        variables=sol_dict,
                        objective=result.objective if hasattr(result, 'objective') else None,
                        is_optimal=result.status == minizinc.Status.OPTIMAL_SOLUTION
                    ))
            elif result.status == minizinc.Status.OPTIMAL_SOLUTION:
                sol_dict = {}
                for key in result.solution.__dict__:
                    if not key.startswith('_'):
                        sol_dict[key] = result.solution.__dict__[key]
                solutions.append(Solution(
                    variables=sol_dict,
                    objective=result.objective if hasattr(result, 'objective') else None,
                    is_optimal=True
                ))

            return SolveResult(
                solutions=solutions,
                status=str(result.status),
                solve_time=result.statistics.get('solveTime', 0) if hasattr(result, 'statistics') else 0,
                num_solutions=len(solutions),
                error=None
            )

        except Exception as e:
            return SolveResult(
                solutions=[],
                status="ERROR",
                solve_time=0,
                num_solutions=0,
                error=str(e)
            )

    @mcp.tool()
    async def list_solvers() -> List[SolverInfo]:
        """
        List all available MiniZinc solvers on the system.
        """
        solvers = []
        try:
            # Get all available solvers
            for solver_id in minizinc.Solver.available():
                try:
                    solver = minizinc.Solver.lookup(solver_id)
                    solvers.append(SolverInfo(
                        id=solver.id,
                        name=solver.name,
                        version=solver.version,
                        tags=solver.tags if hasattr(solver, 'tags') else []
                    ))
                except:
                    # Skip if we can't load the solver info
                    continue
        except Exception as e:
            # If MiniZinc is not installed, return an empty list
            pass

        return solvers

    @mcp.tool()
    async def validate_model(model_str: str) -> Dict[str, Any]:
        """
        Validate a MiniZinc model syntax without solving it.

        Returns information about the model including variables, constraints,
        and any syntax errors.
        """
        try:
            model = minizinc.Model()
            model.add_string(model_str)

            # Try to create an instance with the default solver
            solver = minizinc.Solver.lookup("gecode")
            instance = minizinc.Instance(solver, model)

            return {
                "valid": True,
                "error": None,
                "message": "Model is syntactically valid"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "message": "Model validation failed"
            }


    return mcp

app = create_server()

if __name__ == "__main__":
    app.run(transport="sse", host="0.0.0.0", port=8000)