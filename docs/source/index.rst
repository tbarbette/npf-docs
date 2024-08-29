.. _index:

=================================================
Network Performance Framework (NPF) documentation
=================================================

`NPF <https://github.com/tbarbette/npf>`_ runs performance tests on network software by running snippets of bash scripts on a cluster
following a simple definition script. For instance, the following test script for iPerf3 throughput (omitting graph styling options):

.. code-block:: bash

   %info
   IPerf 2 Throughput Experiment

   %config
   n_runs=5
   var_names={PARALLEL:Number of parallel connections,WINDOW:Window size (kB),THROUGHPUT:Throughput}

   %variables
   PARALLEL=[1-8]
   WINDOW={16,512}
   TIME=2

   %script@server
   iperf -s

   %script@client delay=1
   //Launch the program, copy the output to a log
   iperf -c ${server:0:ip} -w ${WINDOW}k -t $TIME -P $PARALLEL 2>&1 | tee iperf.log
   //Parse the log to find the throughput
   result=$(cat iperf.log | grep -ioE "[0-9.]+ [kmg]bits" | tail -n 1)
   //Give the throughput to NPF through stdout
   echo "RESULT-THROUGHPUT $result"


Can be run with the following command line:

.. code-block:: bash

   npf-run --test tests/tcp/01-iperf.npf --cluster client=machine01.cluster.com server=machine02.cluster.com

To produce the following graph:

.. tabs::

   .. tab:: Default

      This is the default graph, with almost no configuration, generated out of the data automatically. 
      The default is not always a lineplot. NPF selected a lineplot because of the number of variables and points.
      
      .. image:: https://github.com/tbarbette/npf/raw/master/tests/tcp/iperf2-THROUGHPUT.svg
         :width: 500
         :alt: Result for tests/tcp/01-iperf.npf, by default it gives a lineplot

   .. tab:: Boxplot

      Forcing the graph type to boxplot

      .. image:: https://github.com/tbarbette/npf/raw/master/tests/tcp/iperf2-THROUGHPUT-boxplot.svg
         :width: 500
         :alt: Result for tests/tcp/01-iperf.npf with a boxplot

   .. tab:: Barplot

      Forcing the graph type to barplot

      .. image:: https://github.com/tbarbette/npf/raw/master/tests/tcp/iperf2-THROUGHPUT-barplot.svg
         :width: 500
         :alt: Result for tests/tcp/01-iperf.npf with a barplot

   .. tab:: Horizontal barplot

      Forcing the graph type to be an horizontal barplot

      .. image:: https://github.com/tbarbette/npf/raw/master/tests/tcp/iperf2-THROUGHPUT-barh.svg
         :width: 500
         :alt: Result for tests/tcp/01-iperf.npf with an horizontal barplot

   .. tab:: [...]

      See the :ref:`Graphing page <graph>`.


Test scripts defines variables for which NPF runs tests to evaluate their combinations
and report performance results.

NPF will output the results in configurable :ref:`CSV files <cluster>`. Below, two example of CSV outputs:

.. tabs::
   
   .. tab:: Single output
      
      The format given with ``--single-output`` is inteded to use Pandas and post-process the data by yourself. It gives you the result of every runs, for every variables.

      .. csv-table:: CSV example
         :header-rows: 1

         index,build,test_index,PARALLEL,WINDOW,TIME,THROUGHPUT,run_index
         0,local,0,1,16,2,6743098654.72,0
         1,local,0,1,16,2,9899899617.28,1
         2,local,0,1,16,2,9320079032.32,2
         3,local,0,1,16,2,10350871183.36,3
         4,local,0,1,16,2,9212704849.92,4
         5,local,1,2,16,2,6506875453.44,0
         6,local,1,2,16,2,16965120819.2,1
         7,local,1,2,16,2,16857746636.8,2
         8,local,1,2,16,2,17609365913.6,3
         9,local,1,2,16,2,16642998272.0,4
         10,local,2,3,16,2,20937965568.0,0
         11,local,2,3,16,2,19864223744.0,1
         ...

   .. tab:: Multiple output

      This format is more configurable, to give CSV per output variable, and one CSV per series. This one is for the iperf throughput, exported with ``--output --output-columns x mean std``

      There will be one file for ``WINDOW=16`` and one for ``WINDOW=512``
      
      .. csv-table:: WINDOW=16
         :header-rows: 0
         :delim: space

         1 9105330667.52 1250639608.3643892
         2 14916421419.008001 4217093640.431153
         3 22312355102.719997 2218673850.7652254
         4 28475633172.48 2547643401.7214246
         5 33135672688.640003 4197547808.1855946
         6 37194416783.36 3457115197.0040603
         7 44560285696.0 6039356316.673344
         8 47223165419.520004 7102751440.813944

      .. csv-table:: WINDOW=512
         :header-rows: 0
         :delim: space

         1 25383256719.36 3269962568.948725
         2 55641301319.68001 10321647319.401031
         3 68397354188.8 8960180907.481855
         4 91847875624.95999 2907918066.8286467
         5 96851512524.8 3153219791.852363
         6 99192269701.12 873368689.2990192
         7 99514392248.32 1317512283.5617392
         8 98827197480.96 2457532097.396189


NPF automatically builds graphs, computes :ref:`statistics <stats>`  result for each test
showing the importance of each factor, the min/max values, or average for each factor levels.

.. code-block:: text

   Feature importance:
      PARALLEL : 0.3966
      WINDOW : 0.6034

   Max:
      PARALLEL = 7, WINDOW = 512, TIME = 2 : 99514392248.32
   Min:
      PARALLEL = 1, WINDOW = 16, TIME = 2 : 9105330667.52

   Means and std/mean per variables :
   PARALLEL:
      1 : 17244293693.44
      2 : 35278861369.34
      3 : 45354854645.76
      4 : 60161754398.72
      5 : 64993592606.72
      6 : 68193343242.24
      7 : 72037338972.16
      8 : 73025181450.24

   WINDOW:
      16 : 29615410118.66
      512 : 79456894976.00

NPF can be used to compare different softwares, or the evolution of
performances through commits.

.. tabs::

   .. tab:: History

      TODO

   .. tab:: Comparison

      TODO

NPF can also generate a website that will allow to explore the data, and share an interactive graph that can be directly linked from a paper.

TODO : demo of website

With the ``--notebook <path>`` parameter, NPF can output a :ref:`Jupyter Notebook <notebooks>` that produces the graphs and gives a starting point for further analysis or fine tuning of the graphs. The following image shows the Jupyter Notebook generated by NPF for the iPerf3 throughput test.

.. image:: /_static/jupyter-iperf.png
   :width: 500
   :alt: Jupyter Notebook for tests/tcp/01-iperf.npf

NPF can execute tests on a computer cluster, running your tests
in multiple configurations rapidly and on relevant hardware.

.. tabs::

   .. tab:: Localhost

      TODO

   .. tab:: Local Cluster`

      TODO

   .. tab:: Grid5000

      TODO

   .. tab:: CloudLab

      TODO

Test scripts are easy to write and share. We encourage users to share their ``.npf`` scripts along with their code to allow other users to reproduce their results and graphs.

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
   jinja
   stats
   output
   notebooks
   graph
   repos
   cluster
   api