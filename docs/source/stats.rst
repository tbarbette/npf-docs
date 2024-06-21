.. _stats:
Statistics
==========

If you have many variables, graphs will not be useful. The ``--statistics`` argument will generate some statistical information.

This is the result of ``--statistics`` with the iperf example.

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

The feature importance is built using the entropy of a regression tree. It shows the importance of most variables. Here WINDOW is more important that PARALLEL, but arguably they're both important and actually do contribute to the THROUGHPUT metric.

TODO

