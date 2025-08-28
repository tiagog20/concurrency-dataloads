import os
#Typing sirve para definir tipos de datos
import typing as t
#Request sirve para hacer peticiones HTTP
import requests
#utils sirve para importar las funciones del otro archivo
import utils
import threading
from concurrent.futures import ThreadPoolExecutor

# Sincronización para la escritura de archivos
lock = threading.Lock()

def download_and_save_sprite(pokemon, output_dir):
    """Download and save a single pokemon."""
    with requests.Session() as session:
        content = utils.maybe_download_sprite(session, pokemon["Sprite"])
        if content is not None:
            target_dir = os.path.join(output_dir, pokemon["Type1"])
            with lock:
                utils.maybe_create_dir(target_dir)
                filepath = os.path.join(target_dir, pokemon["Pokemon"] + ".png")
                utils.write_binary(filepath, content)

@utils.timeit
def main(output_dir: str, inputs: t.List[str]):
    """Download for all intpus and place them in output_dir."""
    utils.maybe_create_dir(output_dir)
    all_pokemons = list(utils.read_pokemons(inputs))
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(download_and_save_sprite, pokemon, output_dir) for pokemon in all_pokemons]
        for future in futures:
            future.result()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="directory to store the data")
    parser.add_argument("inputs", nargs="+", help="list of files with metadata")
    args = parser.parse_args()
    utils.maybe_remove_dir(args.output_dir)
    main(args.output_dir, args.inputs)