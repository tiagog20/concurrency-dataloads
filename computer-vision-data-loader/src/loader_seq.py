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

# Record the start time
start_time = time.time()


@dataclasses.dataclass
class Row:
    image: NDArray[np.uint8]
    name: str


def download(source: str) -> bytes:
    response = requests.get(source)
    return response.content

def load(
    sources: Sequence[Annotated[pathlib.Path, "CSV File"]],
    *,
    downloader: Callable[[str], bytes] = download,
) -> Iterator[Row]:
    for filepath in sources:
        # Read the CSV file using pandas
        df = pd.read_csv(filepath)

        # Iterate over each row of the DataFrame
        for record in df.itertuples(index=False):
            # Get the name and the sprite URL
            pokemon_name =str(record.Pokemon)
            sprite_url = str(record.Sprite)            
            image_bytes = downloader(sprite_url)
            image_array = imageio.imread(image_bytes)
            yield Row(image=image_array, name=pokemon_name)
            
if __name__ == '__main__':
    csv_file_path = pathlib.Path("C:/Users/Santiago/Documents/EAFIT/Grandes Volumenes de Datos/computer-vision-data-loader/data/pokemon-gen1-data.csv")
    pokemon_dataloader = load([csv_file_path])#
    pokemon_batch = list(pokemon_dataloader)
    num_to_display = len(pokemon_batch)

    rows = 13
    cols = 12

    fig, axes = plt.subplots(rows, cols, figsize=(15, 15))
    axes = axes.flatten()

    for i, pokemon_row in enumerate(pokemon_batch):
        ax = axes[i]
        ax.imshow(pokemon_row.image)
        ax.set_title(f"#{i+1}: {pokemon_row.name}", fontsize=8)
        ax.axis('off')

    for j in range(num_to_display, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time:.2f} seconds")
