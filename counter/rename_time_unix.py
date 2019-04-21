import os
import sys
from tqdm import tqdm
from datetime import datetime

src = sys.argv[1]

src_files = os.listdir(src)
src_files = [file for file in src_files if file.endswith('jpg')]

for file in tqdm(src_files):
    time = file[:15]
    # print(time)
    try:
        name = datetime.strptime(time, "%Y-%m-%d_%H%M").strftime("%s")
        os.rename(f'{src}/{file}', f'{src}/{name}.jpg')
    except ValueError:
        pass
    # print(name)