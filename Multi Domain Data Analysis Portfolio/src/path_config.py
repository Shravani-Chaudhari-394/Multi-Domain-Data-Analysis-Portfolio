

import sys
import os


def _find_project_root(start: str, markers=("src", "data")) -> str:
    """
    Walk UP from `start` until we find a directory that contains
    ALL of the `markers` as sub-directories.  That is the project root.
    """
    current = os.path.abspath(start)
    for _ in range(8):
        if all(os.path.isdir(os.path.join(current, m)) for m in markers):
            return current
        parent = os.path.dirname(current)
        if parent == current:   # reached filesystem root
            break
        current = parent
    # Fallback: return the starting directory
    return os.path.abspath(start)


# ── Resolve paths ────────────────────────────────────────────────────────────
# os.getcwd() is the notebook's directory when running inside Jupyter
PROJECT_ROOT: str = _find_project_root(os.getcwd())
SRC_PATH:     str = os.path.join(PROJECT_ROOT, "src")
DATA_DIR:     str = os.path.join(PROJECT_ROOT, "data")

# Ensure src/ is on sys.path so all shared modules are importable
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


def make_output_dir(project_name: str) -> str:
    """
    Create and return  <project_root>/outputs/<project_name>/
    with sub-folders  figures/  and  reports/  already created.

    Usage (in a notebook):
        OUTPUT_DIR = make_output_dir("project2")
    """
    out = os.path.join(PROJECT_ROOT, "outputs", project_name)
    os.makedirs(os.path.join(out, "figures"), exist_ok=True)
    os.makedirs(os.path.join(out, "reports"), exist_ok=True)
    return out


def data_path(filename: str) -> str:
    """
    Return the full path to a file inside the data/ directory.

    Usage:
        df = pd.read_csv(data_path("StudentsPerformance.csv"))
    """
    return os.path.join(DATA_DIR, filename)


# ── Print a summary when imported ────────────────────────────────────────────
def print_paths() -> None:
    print(f"📁 Project root : {PROJECT_ROOT}")
    print(f"📁 src/         : {SRC_PATH}  (on sys.path)")
    print(f"📁 data/        : {DATA_DIR}")
