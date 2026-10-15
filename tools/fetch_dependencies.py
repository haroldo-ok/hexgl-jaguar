#!/usr/bin/env python3
"""Populate absent vendor sources using exact locked upstream commits."""
from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1]
for name,info in json.loads((R/'dependencies.lock.json').read_text()).items():
    dest=R/'vendor'/name
    if dest.exists():
        print('Keeping supplied source:',name);continue
    dest.mkdir(parents=True)
    def git(*args):subprocess.run(['git','-C',str(dest),*args],check=True)
    git('init');git('remote','add','origin',info['url'])
    git('fetch','--depth','1','origin',info['commit'])
    git('checkout','--detach','FETCH_HEAD')
