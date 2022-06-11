.. _index:

=================================================
Network Performance Framework (NPF) documentation
=================================================

`NPF <https://github.com/tbarbette/npf>`_ runs performance tests on network software by running snippets of bash scripts on a cluster
following a simple definition script. For instance, the following test script for iPerf3 throughput (omitting graph styling options):

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

Can be run with the following command line:

.. code-block:: bash

   npf-run --test tests/tcp/01-iperf.npf

To produce the following graph:

.. image:: https://github.com/tbarbette/npf/raw/master/tests/tcp/01-iperf-THROUGHPUT.png
   :width: 400
   :alt: Result for tests/tcp/01-iperf.np

Test scripts defines variables for which NPF runs tests to evaluate their combinations
and report performance results.

NPF builds graphs and computes statistical result for each test 
showing the difference between variables values, different softwares, or the evolution of
performances through commits.

NPF can execute tests on a computer cluster, running your tests
in multiple configurations rapidly and on relevant hardware.

Test scripts are easy to write and share.
We encourage users to share their ``.npf`` scripts along with their code 
to allow other users to reproduce their results and graphs.

The documentation describes first the basic :doc:`usage <usage>` and :ref:`installation <installation>` of NPF.
It then elaborates on writing ``.npf`` :ref:`tests <tests>` scripts, with the definition of :ref:`variables <variables>`
and advanced configuration for :ref:`graphs <graph>` generation.
NPF can also compile and deploy code as specified in :ref:`repositories <repos>`.
Finally, computer clusters can be specified to NPF in :ref:`cluster <cluster>` files.

Contents
--------

.. toctree::
   usage
   tests
   variables
   graph
   repos
   cluster
