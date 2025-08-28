Pokémon Concurrency Benchmark
Overview

This activity evaluates different concurrency methods in Python to determine the most efficient approach for downloading and processing a dataset of 151 Pokémon names and sprites hosted on GitHub. The study compares asyncio, multiprocessing, threading, and sequential execution, analyzing their performance through repeated trials. Additionally, a dataloader implementation was developed to optimize memory usage while loading images.

Objective

To identify the fastest concurrency method for downloading and processing Pokémon data.

To evaluate the consistency and reliability of each method through multiple runs.

To measure the impact of a dataloader on execution and memory performance.

Methods Evaluated

Asyncio

Average execution time: ~1.3s

Most efficient method with stable performance across runs.

Multiprocessing

Average execution time: ~3.1s

Competitive performance, slower than asyncio but faster than threading and sequential.

Threading

Average execution time: ~14.0s

Consistent but significantly slower than asyncio and multiprocessing.

Sequential

Average execution time: ~13.7s

Slowest method overall, confirming its limitations for scalable workloads.

Dataloader Experiment

To further explore efficiency, a dataloader was implemented for each method.
The results are summarized below:

Method	Data Loading Time (s)	Total Execution Time (s)	Relative Performance*
Asyncio	1.77	7.08	1x (baseline)
Multiprocessing	14.45	17.69	~2.5x slower
Threading	15.65	18.78	~2.6x slower
Sequential	90.54	167.59	~23.6x slower

*Relative performance calculated against the fastest method (asyncio).

Key Findings

Asyncio consistently outperformed all other methods, both in direct concurrency tests and with the dataloader.

Multiprocessing offered a good balance of speed and reliability, but was still slower than asyncio.

Threading showed stable results but no significant advantages over multiprocessing.

Sequential execution was consistently the least efficient.

Expressing results as “times slower than asyncio” provides a clearer perspective than percentages.

Conclusion

The study demonstrates that asyncio is the most suitable concurrency method for downloading and processing large numbers of Pokémon images. It ensures scalability, speed, and consistency, making it the recommended choice for larger datasets or time-sensitive tasks. Multiprocessing remains a strong alternative when CPU-bound tasks are involved, while threading and sequential approaches are less efficient and not recommended for this context.

Author

Santiago González-Granada
EAFIT – Big Data Course (Grandes Volúmenes de Datos)
