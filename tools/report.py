#!/usr/bin/env python3
"""Compatibility entry point for the current dual-layer regression report."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('black_screen_report.py')),run_name='__main__')
