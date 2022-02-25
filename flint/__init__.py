"""
# Flint
## CLI tool for Fire-Watch
"""

import os

__version__ = "0.1.0"

domain = "fire-watch-lite.herokuapp.com"
protocal = "https://"

if os.getenv("CI"):
    domain = "localhost:8000"
    protocal = "http://"
