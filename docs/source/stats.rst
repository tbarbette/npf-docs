.. _stats:

Interpretation of results
=========================

The :ref:`graph` section gives means to try to arrange graphs, splitting a graph in sub-graphs for
levels of a variable, ignoring less important variables, ...

But if you have many variables and results, graphs will be hard to comprehend.
It might be best to use statistical tools to reduce the search space and conduct
a more restricted experimental design (see :ref:`variables`).

Statistics
----------
The ``--statistics`` argument will generate some statistical information.

This is the result of ``--statistics`` with the `01-iperf-advanced.npf` example which
is using the iPerf tool to measure the performance of local TCP connections. Compared to the front page
example, this version has more variables, such as the number of CPU allocated to the iperf software.

The statistics are generated in two parts. First, for each metric observed (THROUGHPUT, L1 misses, etc...), some quantification is proposed.
.. As with many observations this would quickly sum up to a lot of text, only observations with
Then, a correlation matrix is built for all metrics at once.



.. code-block:: text

   Building dataset...
   Statistics for THROUGHPUT
   Learning dataset built with 6144 samples and 6 features...
   No tree graph when maxdepth is > 8. Use --statistics-maxdepth 8 to fix it to 8.

   Feature importance:
   CONGESTION : 0.0017
   NODELAY : 0.0025
   PARALLEL : 0.2349
   CPU : 0.2898
   WINDOW : 0.4711

   Max:
   PARALLEL = 8, CPU = 8, WINDOW = 512, CONGESTION = reno, NODELAY = Nagle enabled, TIME = 2 : 272730423296.00
   Min:
   PARALLEL = 1, CPU = 5, WINDOW = 4, CONGESTION = bbr, NODELAY = Nagle enabled, TIME = 2 : 17406361.60

   Means per variables:
   PARALLEL:
      1 : 23406949034.67
      2 : 41691482521.60
      3 : 55738238730.24
      4 : 64936604357.97
      5 : 69935443312.64
      6 : 73196809803.09
      7 : 73895472223.57
      8 : 71723332840.11

   CPU:
      1 : 10506062342.83
      2 : 29201748241.07
      3 : 43929965499.73
      4 : 53619540923.73
      5 : 70731434530.13
      6 : 84852326263.47
      7 : 89814343543.47
      8 : 91868911479.47

   WINDOW:
      1 : 104438169.60
      2 : 104145715.20
      4 : 104596548.27
      8 : 104852411.73
      16 : 104377548.80
      32 : 106264166.40
      64 : 99640165444.27
      128 : 93488939008.00
      256 : 94197328991.57
      512 : 94784307855.36
      1024 : 94311106478.08
      2048 : 94559996477.44
      4096 : 94357551404.37
      8192 : 94045998503.25
      16384 : 94278390906.88
      32768 : 94756206018.56

   CONGESTION:
      bbr : 60031966392.32
      cubic : 58966340638.72
      reno : 58948317777.92

   NODELAY:
      Nagle disabled : 57695090414.93
      Nagle enabled : 60935992791.04


   Correlation matrix:
            PARALLEL   CPU WINDOW CONGESTION NODELAY  THROUGHPUT
   PARALLEL       1.00 -0.00  -0.00      -0.00   -0.00        0.23
   CPU                  1.00   0.00       0.00    0.00        0.41
   WINDOW                      1.00       0.00    0.00        0.25
   CONGESTION                             1.00   -0.00       -0.01
   NODELAY                                        1.00        0.02
   THROUGHPUT                                                 1.00
   Graph of correlation matrix saved to doc/covariance-THROUGHPUT-correlation.png

   P-value of ANOVA (low p-value indicates a probable interaction):
            PARALLEL  CPU WINDOW CONGESTION NODELAY  THROUGHPUT
   PARALLEL            0.00   0.00       0.24    0.36        0.00
   CPU                        0.00       0.88    0.16        0.00
   WINDOW                                0.74    0.29        0.00
   CONGESTION                                    0.37        0.51
   NODELAY                                                   0.02
   Graph of a ANOVA matrix saved to doc/covariance-THROUGHPUT-anova.png
   Generating graphs...
   Pandas dataframe written to doc/covariance.csv
   Graph of test written to /etinfo/users2/tbarbette/workspace/npf/doc/covariance-THROUGHPUT.png

Feature importance
^^^^^^^^^^^^^^^^^^

The feature importance is built using the entropy of a regression tree.
It shows the importance of most variables. Here ``WINDOW`` is more important than ``PARALLEL``, but arguably they're both important and do contribute to the ``THROUGHPUT`` metric.

The regression tree is saved to a PDF file for visualization. In the example above, it is not generated because the tree is too deep.
Use `--statistics-maxdepth 5` to limit the tree depth.

.. image:: https://github.com/tbarbette/npf/raw/main/doc/covariance-THROUGHPUT-clf.png
   :width: 400
   :alt: Regression tree

The tree can be read as the most significant decisions to reach the best (or worst) performance.

Max/min and features per variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The next lines show the variables for the best and the worst values.

Then, for each parameter, the mean of the result (in this case the throughput) for each parameter.

Interactions with ANOVA
^^^^^^^^^^^^^^^^^^^^^^^

Finally, the last available statistic is the p-value of a two-way ANOVA test for each pair of variables.

.. image:: https://github.com/tbarbette/npf/raw/main/doc/covariance-THROUGHPUT-anova.png
   :width: 400
   :alt: ANOVA p-value matrix

It shows the possible interaction between each pair of variables. If the P value is smaller than 0.05 there is a probable interaction. A value higher than 0.05 only means there is no clear linear interaction between variables.


Correlation matrix for all parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All the other statics are per-metric, a correlation matrix is then built for all metrics at once.
The correlation matrix then shows the pearson correlation between each factor and each observation.

The correlation matrix is printed textually but also generated as a picture.

.. image:: https://github.com/tbarbette/npf/raw/main/doc/covariance-THROUGHPUT-correlation.png
   :width: 400
   :alt: Correlation matrix

Correlation matrix are symmetrical. It shows in this cas the parameters have no correlation between themselves,
but the interesting part is for the correlation between factors and results. We find again a notion of
importance of the factors towards the throughput.
