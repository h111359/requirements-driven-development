#!/usr/bin/env python3
"""Print the current system time in YYYYMMDD-hhmiss format.

This script is intended to be used as a deterministic building block from other
RDD action scripts.

Output:
  A single line to stdout, e.g. `20251217-154203`.
"""

from __future__ import annotations

from datetime import datetime


def main() -> None:
    # Local system time.
    print(datetime.now().strftime("%Y%m%d-%H%M%S"))


if __name__ == "__main__":
    main()
