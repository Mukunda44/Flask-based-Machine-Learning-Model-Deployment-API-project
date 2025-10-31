# tests/conftest.py
import sys
from pathlib import Path

# Add project root (the folder that contains the 'app' package) to sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
