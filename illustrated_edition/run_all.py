"""Run the scientific illustration scripts in a documented order."""
from pathlib import Path
import subprocess
import sys
root=Path(__file__).resolve().parent
(root/'reviews').mkdir(exist_ok=True)
for name in ['download_coordinates.py', *(f'draw_ch{n:02d}.py' for n in range(1,9)), 'render_experimental_structures.py', 'draw_data_plates.py']:
    print(name, flush=True)
    subprocess.run([sys.executable,str(root/name)],check=True)
