import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    'src/__init__.py',
    'src/helper.py',
    'src/prompt.py',
    '.env',
    'setup.py',
    'app.py',
    'research/trails.ipynb'
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir = filepath.parent  # This gets the directory of the file

    # Create directory if it doesn't exist
    if filedir != Path(''):  # Skip if file is in root (e.g., .env, setup.py)
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filepath.name}")

    # Create empty file if it doesn't exist
    if not filepath.exists():
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filepath.name} already exists.")
