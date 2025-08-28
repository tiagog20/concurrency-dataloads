import atexit
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import requests
import utils
import typing as t
import os

session: requests.Session

def download_site(url, output_dir):
    content = utils.maybe_download_sprite(session, url["Sprite"])
    if content is not None:
            target_dir = os.path.join(output_dir, url["Type1"])
            utils.maybe_create_dir(target_dir)
            filepath = os.path.join(target_dir, url["Pokemon"] + ".png")
            utils.write_binary(filepath, content)
            name = multiprocessing.current_process().name
            print(f"{name}: Read {len(content)} bytes from {url['Sprite']}")
    
def download_all_sites(sites, output_dir): 
    with ProcessPoolExecutor(initializer=init_process) as executor:
        futures = [executor.submit(download_site, site, output_dir) for site in sites]
        # Wait for all tasks to complete
        for future in futures:
            future.result()

def init_process():
    global session
    session = requests.Session()
    atexit.register(session.close)

@utils.timeit
def main(output_dir: str, inputs: t.List[str]):
    """Download for all inputs and place them in output_dir."""
    utils.maybe_create_dir(output_dir)
    sites = utils.read_pokemons(inputs)
    download_all_sites(sites, output_dir)
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="directory to store the data")
    parser.add_argument("inputs", nargs="+", help="list of files with metadata")
    args = parser.parse_args()
    utils.maybe_remove_dir(args.output_dir)
    main(args.output_dir, args.inputs)