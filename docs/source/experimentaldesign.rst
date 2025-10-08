.. _expdesign:

Experimental design
===================

If there are many levels (values) for many factors (variables), then the default grid-search (or full factorial) algorithm might
take too much time to complete. NPF makes it easy to use a random or space-filling experimental design to explore the design space and
find the important factors to conduct further detailed experiments on specific factors.

Cache
-----
NPF includes a caching of results. Just add `--cache` to the value of previous experiments. Therefore, if you explore "CPU=[1-4]" and then design to look for "CPU=[1-8]", only the experiment for CPU = 5 to 8 would run.
This enables very fast exploration of the experimental design. The cache is tied to the current version of the repository given to the command line, so if the software is updated the results are expected to change.

Of course, reproducibility imposes to never use `--cache` for final experiment data and ensure every results are consistent. But this feature is extremely useful for the research phase.

If you want to only get results from the cache without running any supplementary tests, use `--no-test`.

.. note::
    Before NPF v2 "cache" was the default behavior and was enabled by default. Use `--force-retest` on v1 to disable caching.

Space-filling design
--------------------
NPF has support for multiple space-filling designs. We categorize them as offline and online. Offline designs do not depend on the results of the previous run, such as the default grid search, random exploration or 2-k. Online-design depend on the result of the last exploration.

Space filling designs are enabled with the ``--exp-design`` command-line. If not given, grid-search is used.

We will use a simple example with two factors, "CPU" and "FREQ" which set the number of CPU cores and the frequency of the CPU. The values are given as a list of integers, such as ``CPU=[1-16]`` and ``FREQ=[1000-2000#100]``. The default is to use grid-search, which will try every combination of the factors, that is 16*11 = 176 runs.

Offline designs
^^^^^^^^^^^^^^^

Offline designs do not use the result of past experiments to decide on the next experiment to run.

Grid-search
...........
``--exp-design grid`` will use grid-search. Every factors will be tried using a cross-product of their levels. In the example above, NPF will start with CPU=1, FREQ=1000, then CPU=1, FREQ=1100, then CPU=1, FREQ=1200, and so on until CPU=16, FREQ=2000. This is the default behavior.

Random exploration
..................
``--exp-design random`` will use a random exploration of the design space. It will randomly select a value for each factor, and run the experiment. This is useful to quickly explore the design space and find the important factors.

Online designs
^^^^^^^^^^^^^^^

Zero-loss throughput
....................
``--exp-design zlt(INPUT,OUTPUT)`` will try to find the minimal input that gives the same output. This is typically used to search for a "zero-loss" throughput. ``INPUT`` must be a variable with multiple values, like a range ``[1-100]``. The algorithm will start with the largest input and look at the given ``OUTPUT``. It will then try the value below the output as input. For instance, if for input=100, the output is 47, then the next value to be tried will be 46.

In some cases, you may want to try all values that are sustained by the system. Imagine the system can absorb 46 Gbps of traffic and you want to observe the latency, then you want to try all values below 46 and not just find the limit (zero-loss throughput) which is 46. Use ``--exp-design allzlt(INPUT,OUTPUT)`` instead.

If output is given as a percentage of the input and not a raw value comparable to the input, you can use the suffix ``p`` instead of ``t`` like ``zlp`` or ``allzlp``.

Constraints
~~~~~~~~~~~
Constraints are variables for which a higher value, all other parameters being equal, can only improve performance. For instance, the number of cores is a usual constraint in a system which is relatively horizontally scalable.
Giving such "monotonic" constraints to the experimental design can significantly reduce the number of experiments to run.
Imagine the ZLT is 14MPPS with 4 cores and the system has not much inter-core contention. There's no need to try 15 and 16MPPS with 3 cores as 3 cores cannot do better than 4 cores.

``--exp-design allzlt(INPUT,OUTPUT,1.01,CPU)``

will try to find the zero-loss throughput for INPUT given OUTPUT, but will try first with the highest CPU value. When the ZLT is found for a given CPU value, it will start at the max ZLT for the previous CPU value, as a system with less cores cannot perform better than a system with more cores.

Multiple constraints can be given, separated by commas.

``--exp-design allzlt(INPUT,OUTPUT,1.01,CPU,FREQ)``

will try first the highest CPU with then the highest FREQ, and will then assume that any configuration with less CPU but the same FREQ cannot de better, and similarly that any configuration with less FREQ but the same CPU cannot be better.


Mininmum Acceptable
...................

``--exp-design minacceptable(FACTOR,OUTPUT_PERCENT,1.01)``
will try to find the minimum FACTOR that has OUTPUT_PERCENT >= 100/MARGIN.
The exploration starts with the lowest FACTOR and increase it using a binary search until the OUTPUT_PERCENT is above the threshold.
If the lowest value of FACTOR gave, e.g. 50% of OUTPUT_PERCENT, then the next value to be tried will be the middle value between the lowest and the highest value of FACTOR. It is a binary search that assumes a certain proportionality between FACTOR and OUTPUT_PERCENT.
This is useful to find the minimum resources required to sustain a given throughput.