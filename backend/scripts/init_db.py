"""
Create and seed the GEODIA SQLite database.
Usage: python scripts/init_db.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.seed_db import main as seed_main

if __name__ == "__main__":
    seed_main()
