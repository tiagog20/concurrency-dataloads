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
from concurrent.futures import ThreadPoolExecutor
import os
import sys

@dataclasses.dataclass
class Row:
    """Represents a single row of data with an image and a name."""
    image: NDArray[np.uint8]
    name: str

def download(source: str) -> bytes:
    """Downloads content from a URL and returns it as bytes."""
    response = requests.get(source)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.content

def _load_single_row_tuple(record_tuple, downloader: Callable[[str], bytes]) -> Row:
    pokemon_name, sprite_url = record_tuple
    print(f"Loading {pokemon_name}...") # Add this line
    try:
        image_bytes = downloader(sprite_url)
        image_array = imageio.imread(image_bytes)
        print(f"Loaded {pokemon_name}") # Add this line
        return Row(image=image_array, name=pokemon_name)
    except Exception as e:
        print(f"Error loading {pokemon_name}: {e}", file=sys.stderr)
        return Row(image=np.zeros((96, 96, 3), dtype=np.uint8), name=f"{pokemon_name} (Error)")
def load(
    sources: Sequence[Annotated[pathlib.Path, "CSV File"]],
    *,
    downloader: Callable[[str], bytes] = download,
    max_workers: int = 10,
) -> Iterator[Row]:
    """
    Creates a parallel dataloader for the Pokémon dataset using threading.

    Args:
        sources: A sequence of file paths to the CSV files.
        downloader: The function to use for downloading image content.
        max_workers: The number of threads to use.
    
    Yields:
        A `Row` object for each Pokémon.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for filepath in sources:
            df = pd.read_csv(filepath)
            records = list(zip(df['Pokemon'], df['Sprite']))
            
            yield from executor.map(lambda rec: _load_single_row_tuple(rec, downloader), records)


if __name__ == '__main__':
    # Record the start time
    start_time = time.time()
    
    # Path to the CSV file
    csv_file_path = pathlib.Path("C:/Users/Santiago/Documents/EAFIT/Grandes Volumenes de Datos/computer-vision-data-loader/data/pokemon-gen1-data.csv")
    
    # Load all data using the threading data loader
    pokemon_dataloader = load([csv_file_path])
    pokemon_batch = list(pokemon_dataloader)

    # Calculate and print data loading time
    loading_time = time.time() - start_time
    print(f"Data loading time (threading): {loading_time:.2f} seconds")

    # Plot the grid of all 151 Pokémon sprites
    num_to_display = len(pokemon_batch)
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

    # Hide any unused subplots
    for j in range(num_to_display, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

    # Calculate and print total execution time
    total_execution_time = time.time() - start_time
    print(f"Total execution time (including plotting): {total_execution_time:.2f} seconds")