import asyncio
import json
import os
import signal
import subprocess
import sys
import time
import urllib.request

import pytest

SERVER_URL = os.environ.get("MCP_SSE_URL", "http://127.0.0.1:8000/sse")


def _start_server():
    # Start the server in a subprocess
    env = os.environ.copy()
    proc = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=os.path.dirname(__file__) + "/..",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    return proc


def _wait_ready(proc, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.2)
            continue
        if "Running" in line or "Uvicorn" in line or "INFO" in line:
            return True
    return False


@pytest.mark.timeout(60)
def test_e2e_solve_constraint():
    proc = _start_server()
    try:
        assert _wait_ready(proc), "Server did not become ready in time"

        # Very simple client: POST JSON to the tool endpoint if available
        # FastMCP uses SSE transport for tools; for a minimal e2e smoke test,
        # just ensure the process is running and the module imports.
        # For full protocol test one would use an MCP client.

        # As a smoke test, we run a short-lived Python snippet that calls the core solver.
        # This still exercises the package in a subprocess and ensures runtime works end-to-end.
        code = r"""
import asyncio
from main import ConstraintModel, solve_constraint_core
async def run():
    problem = ConstraintModel(model='var 1..3: x; solve satisfy;', solver='gecode')
    res = await solve_constraint_core(problem)
    assert res.num_solutions >= 1
asyncio.run(run())
"""
        sub = subprocess.run([sys.executable, "-c", code], cwd=os.path.dirname(__file__) + "/..", check=True)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
