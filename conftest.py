import sys
import pathlib

# Ensure the project src directory is on the Python path for imports
PROJECT_ROOT = pathlib.Path(__file__).parent
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
