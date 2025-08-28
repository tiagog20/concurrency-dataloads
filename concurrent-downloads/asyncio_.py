# async_version.py

import os, typing as t, asyncio, aiohttp, argparse, time

import utils


async def _get(session: aiohttp.ClientSession, url: str) -> bytes | None:

    try:

        async with session.get(url, timeout=aiohttp.ClientTimeout(total=25)) as r:

            return await r.read() if r.status == 200 else None

    except Exception:

        return None


async def download_and_save_pokemon(session, pokemon, output_dir):

    content = await _get(session, pokemon["Sprite"])

    if content:

        target = os.path.join(output_dir, pokemon["Type1"])

        utils.maybe_create_dir(target)

        path = os.path.join(target, pokemon["Pokemon"] + ".png")

        await asyncio.to_thread(utils.write_binary, path, content)


async def dowload_and_save_all_pokemons(pokemons, output_dir):

    sem = asyncio.Semaphore()

    async with aiohttp.ClientSession(headers={"User-Agent": "async-poke/1.0"}) as s:

        async def one(p):

            async with sem:

                await download_and_save_pokemon(s, p, output_dir)

        await asyncio.gather(*(one(p) for p in pokemons))


async def main(output_dir: str, inputs: t.List[str]):

    utils.maybe_create_dir(output_dir)

    pokemons = list(utils.read_pokemons(inputs))  # materialize generator

    start = time.perf_counter()

    try:
# AQUI IBA CONCURRENCY
        await dowload_and_save_all_pokemons(pokemons, output_dir)

    finally:

        elapsed = time.perf_counter() - start

        print(f"Finished {len(pokemons)} downloads in {elapsed:.2f} seconds", flush=True)


if __name__ == "__main__":

    ap = argparse.ArgumentParser()

    ap.add_argument("output_dir")

    ap.add_argument("inputs", nargs="+")

    ap.add_argument("--clean", action="store_true")

    args = ap.parse_args()

    (utils.maybe_remove_dir if args.clean else utils.maybe_create_dir)(args.output_dir)

    # Also time the whole run (belt & suspenders), flushed to stdout.

    t0 = time.perf_counter()

    
    print(f"Total wall time: {time.perf_counter() - t0:.2f} seconds", flush=True)

 