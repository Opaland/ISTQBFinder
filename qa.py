#!/usr/bin/env python3
"""Point d'entrée du QA Knowledge Agent : `python qa.py --help`."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qak.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
