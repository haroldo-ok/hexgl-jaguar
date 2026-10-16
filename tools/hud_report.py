#!/usr/bin/env python3
"""Compatibility entry point for the current verified milestone."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name("frontend_report.py")),run_name="__main__")
