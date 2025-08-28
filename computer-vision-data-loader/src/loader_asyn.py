import dataclasses
import pathlib
import aiohttp
import asyncio
import numpy as np
import pandas as pd
from numpy.typing import NDArray
import imageio
import matplotlib.pyplot as plt
import time
from typing import Annotated, AsyncIterator, Sequence, List, Callable
import sys
import os
import loader

@dataclasses.dataclass
class Row:
    image: NDArray[np.uint8]
    name: str

async def download(session: aiohttp.ClientSession, source: str) -> bytes:
    async with session.get(source) as response:
        response.raise_for_status()
        return await response.read()

async def _load_single_row_tuple(session: aiohttp.ClientSession, record_tuple: tuple[str, str]) -> Row:
    pokemon_name, sprite_url = record_tuple
    try:
        image_bytes = await download(session, sprite_url)
        image_array = imageio.imread(image_bytes)
        return Row(image=image_array, name=pokemon_name)
    except Exception as e:
        print(f"Error loading {pokemon_name}: {e}", file=sys.stderr)
        return Row(image=np.zeros((96, 96, 3), dtype=np.uint8), name=f"{pokemon_name} (Error)")

async def load_async(
    sources: Sequence[Annotated[pathlib.Path, "CSV File"]],
    max_concurrent_downloads: int = 20,
) -> AsyncIterator[Row]:
    async with aiohttp.ClientSession() as session:
        for filepath in sources:
            df = pd.read_csv(filepath)
            records = list(zip(df['Pokemon'], df['Sprite']))
            
            tasks = [
                _load_single_row_tuple(session, record)
                for record in records
            ]
            
            semaphore = asyncio.Semaphore(max_concurrent_downloads)
            
            async def limited_task(task):
                async with semaphore:
                    return await task
            
            for future in asyncio.as_completed([limited_task(task) for task in tasks]):
                yield await future

async def main():
    start_time = time.time()
    csv_file_path = pathlib.Path("C:/Users/Santiago/Documents/EAFIT/Grandes Volumenes de Datos/computer-vision-data-loader/data/pokemon-gen1-data.csv")
    
    pokemon_batch: List[Row] = [row async for row in load_async([csv_file_path])]
        
    loading_time = time.time() - start_time
    print(f"Data loading time (asyncio): {loading_time:.2f} seconds")

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

    for j in range(num_to_display, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

    total_execution_time = time.time() - start_time
    print(f"Total execution time (including plotting): {total_execution_time:.2f} seconds")

if __name__ == '__main__':
    asyncio.run(main())