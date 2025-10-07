import os
import sys
import pathlib
import pytest

# Ensure repository root is importable for `import main`
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

@pytest.fixture(autouse=True, scope="session")
def minizinc_env():
    # Ensure MiniZinc runtime and stdlib are discoverable
    # AppImage extracted to /opt/minizinc
    opt = pathlib.Path("/opt/minizinc")
    if opt.exists():
        lib = opt / "usr" / "lib"
        bin_dir = opt / "usr" / "bin"
        stdlib = opt / "usr" / "share" / "minizinc"
        # Update PATH and LD_LIBRARY_PATH for solvers
        os.environ["PATH"] = f"{bin_dir}:{os.environ.get('PATH','')}"
        ld = os.environ.get("LD_LIBRARY_PATH", "")
        os.environ["LD_LIBRARY_PATH"] = f"{lib}:{ld}" if ld else str(lib)
        # Ensure Python minizinc can find stdlib
        os.environ.setdefault("MINIZINC_DIR", str(stdlib))
