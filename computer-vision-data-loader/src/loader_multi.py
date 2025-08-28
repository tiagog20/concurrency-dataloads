import dataclasses
import pathlib
import requests
from typing import Annotated, Callable, Iterator, Sequence
import numpy as np
import pandas as pd
from numpy.typing import NDArray
import imageio
import matplotlib.pyplot as plt
import time
import multiprocessing
import functools


@dataclasses.dataclass
class Row:
    image: NDArray[np.uint8]
    name: str

def download(source: str) -> bytes:
    response = requests.get(source)
    return response.content

def _load_single_row_tuple(record_tuple, downloader: Callable[[str], bytes]) -> Row:
    pokemon_name, sprite_url = record_tuple
    image_bytes = downloader(sprite_url)
    image_array = imageio.imread(image_bytes)
    return Row(image=image_array, name=pokemon_name)

def load(
    sources: Sequence[Annotated[pathlib.Path, "CSV File"]],
    *,
    downloader: Callable[[str], bytes] = download,
    num_processes: int = multiprocessing.cpu_count(),
) -> Iterator[Row]:
    with multiprocessing.Pool(processes=num_processes) as pool:
        for filepath in sources:
            df = pd.read_csv(filepath)
            records = list(zip(df['Pokemon'], df['Sprite']))
            _partial_load_row = functools.partial(_load_single_row_tuple, downloader=downloader)
            yield from pool.imap_unordered(_partial_load_row, records)

if __name__ == '__main__':
    start_time = time.time()
    csv_file_path = pathlib.Path("C:/Users/Santiago/Documents/EAFIT/Grandes Volumenes de Datos/computer-vision-data-loader/data/pokemon-gen1-data.csv")

    pokemon_dataloader = load([csv_file_path])
    pokemon_batch = list(pokemon_dataloader)

    loading_time = time.time() - start_time
    print(f"Data loading time (multiprocessing): {loading_time:.2f} seconds")

    rows = 13
    cols = 12
    fig, axes = plt.subplots(rows, cols, figsize=(15, 15))
    axes = axes.flatten()

    for i, pokemon_row in enumerate(pokemon_batch):
        if i >= len(axes): break
        ax = axes[i]
        ax.imshow(pokemon_row.image)
        ax.set_title(f"#{i+1}: {pokemon_row.name}", fontsize=8)
        ax.axis('off')

    for j in range(len(pokemon_batch), len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

    total_execution_time = time.time() - start_time
    print(f"Total execution time (including plotting): {total_execution_time:.2f} seconds")