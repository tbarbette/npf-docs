.. _index:

=================================================
Network Performance Framework (NPF) documentation
=================================================

Run performance tests on network software by running snippets of bash scripts on a cluster
following a simple definition file. For instance, the following configuration to test iPerf3 performance (omitting graph styling options):

.. code-block:: bash

   %info
   IPerf3 Throughput Experiment

   %variables
   PARALLEL=[1-8]
   ZEROCOPY={:without,-Z:with}

   %script@server
   iperf3 -s &> /dev/null

   %script@client delay=1
   result=$(iperf3 -f k -t 2 -P $PARALLEL $ZEROCOPY -c ${server:0:ip} | tail -n 3 | grep -ioE "[0-9.]+ [kmg]bits")
   echo "RESULT-THROUGHPUT $result"

Will automatically produce the following graph:

.. image:: https://github.com/tbarbette/npf/raw/master/tests/tcp/01-iperf-THROUGHPUT.png
   :width: 400
   :alt: Result for tests/tcp/01-iperf.np

When launching npf with the following command line:

.. code-block:: bash

   npf-run --test tests/tcp/01-iperf.npf

Test files allow to define a matrix of parameters to try many combinations of
variables for each test and report performance results and evolution for each combination of variables. Check the :ref:`the variables page <variables>` for a description of the possible definitions such as values, ranges, ...

Finally, a graph will be built and statistical results may be computed for each test 
showing the difference between variables values, different softwares, or the evolution of
performances through commits.

Test files are simple to write, and easy to share, as such we encourage
users to share their ".npf" scripts with their code to allow other users to reproduce
their results, and graphs.

NPF supports running the given test across a custer, allowing to try your tests
in multiple different configuration very quickly and on serious hardware.

Check out the :doc:`usage <usage>` section for further information, including
how to :ref:`install <installation>` the project.

Contents
--------

.. toctree::
   usage
   tests
   variables
   graph
   repos
   cluster
