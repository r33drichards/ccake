import os
import pathlib
import pytest

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
