.. _graph:

********
Graphing
********
Graph are automatically generated for all tested variables
combinations.

To choose the type of graph, the number of dynamic variables (I.e. variables that have more than one values) is taken into account, along with the number of series.

For instance, if there is only one dynamic variable, a line plot will be used, with one line per series. If there is no dynamic variables, a barplot will be used, but a box plot can also be used.


Below, npf gave two series to the grapher (current and last commit), while the test script
generate a matrix of Burst and Lengths, that is 2 dynamic variables and only a barplot can render multiple variables at the same time.

.. image:: https://github.com/tbarbette/npf/raw/main/doc/sample_graph.png
   :width: 400
   :alt: Sample graph

If there are 2 dynamic variables, but only a single serie (i.e. you used npf-compare with a single serie, or npf-run with --history 0), one of the variable will be taken out as serie, and a line plot will still be used:

.. image:: https://github.com/tbarbette/npf/raw/main/doc/sample_graph3.png
   :width: 400
   :alt: Sample graph

One can force the graph type with the "graph_type" config option. For instance, if you pass `\-\-config graph_type=boxplot` to the command line, you will get a box plot no matter the number of dynamic variables.

CDF
===

With ``graph_type=cdf``, NPF draws the cumulative distribution function (CDF) of each result: for each value of the variable and each series, the share of the observed results that are at most a given value.
By default, the observed results are the ones of the runs (``n_runs``):

.. code-block:: bash

    %config
    n_runs=20
    graph_type=cdf

    %variables
    X=[1-5]

    %script python-inline
    echo "RESULT-N $(( $X * rand() % 100 ))"

This draws one CDF per value of ``X``, each made of 20 points.
With a single series, as here, each value of the variable has its color, and the legend is titled with the variable.
With several series, each series has its color and each value of the variable its line style.

.. image:: /_static/cdf-N.png
   :alt: CDF of N for each value of X
   :width: 500

The test script is `integration/cdf.npf <https://github.com/tbarbette/npf/blob/main/integration/cdf.npf>`_.

More points per run
    A script can print the same result several times, e.g. one latency per packet. By default, NPF keeps the last value. With ``result_append={N}`` in the ``%config`` section, it keeps all of them, so each value becomes a point of the CDF (see :ref:`tests`, *Handling multiple results*).

Variables that are only noise
    To show how much a result varies over conditions that do not matter individually, for instance with ``LOSS=[0-10]``, run them all and merge them into a single CDF with ``var_aggregate={LOSS:all}``, or ``var_aggregate={LOSS+DELAY:all}`` for several variables (see the *Data transformation* options below).
    NPF reminds it when a CDF graph has more than 4 lines.


Graphing options
================

The graph can be tweaked using many options, and the data can also be transformed using multiple tools to better display results. Data transformation will also affect the output CSV. In any case none of these options affect the values in the data cache, so you may try different tweaks without risks.

All the following options can be added to the ``%config`` section of the test script, or after the ``\-\-config`` parameter on the command line of any of the tools.

* var prefix generally affect variables. It generally takes a list of variables, or a dict of variables->parameters.
* graph prefix only affect the graph, styling ,etc. The CSV data will not be changed.

Graph styling
-------------

Confidence intervals
^^^^^^^^^^^^^^^^^^^^

- **graph_error_fill** =true/false Display a "filling zone" instead of error bars. To be used when you have many points and your graph becomes horrible.
- **graph_error** ={RESULT:type} Confidence interval of the lines of a result: `bar` (standard deviation, the default), `barminmax`, `fill`, `fillminmax`, `fill50` (25th to 75th percentile) or `none`. CDFs have none by default.
- **graph_y_group** ={RESULT:method} How the values of the runs make a point: `mean` (default), `median`, `min`, `max`, `perc95`, `std`, `n`, `first`, `last` or `all`. The key `result` applies to all results.

Line/series style
^^^^^^^^^^^^^^^^^
- **graph_color** ={0,1,2,3} Select a set of color for each serie. Colors are predefined ranges. Default is to use the 0 set of colors for all series, the serie 0 is a mix of different colors, while 1 to 5 are shades of the same colors.
- **graph_markers** ={'o', '^', 's', 'D', '*', 'x', '.', '_', 'H', '>', '<', 'v', 'd'}, type of markers to be used, per-serie. Default if this. See matplotlib docs to find the type.
- **graph_lines** ={'-', '--', '-.', ':'} Type of lines, per-series.
- **graph_fillstyle** =full Fill style of the markers (matplotlib's `fillstyle`).
- **graph_line_params** ={linewidth:2} Arguments given to matplotlib's `plot()` for each line.
- **var_markers** ={RESULT:o;^;s} Markers of the lines of a result, per series, separated by `;`.
- **var_drawstyle** ={RESULT:steps-post} Matplotlib's `drawstyle` of the lines of a result.

Scaling and axis limits
^^^^^^^^^^^^^^^^^^^^^^^

- **var_log**, [THROUGHPUT,LATENCY] Define variables that should be shown in a log axis in base 2
- **var_log_base**, {THROUGHPUT:2} Define variables that should be shown in a log axis, with the specified base (default is 2 with var_log)
- **var_lim**, {THROUGHPUT:0-100} Define the range for some variables, useful to cap graphs. One can produce "broken axis" graphes by giving multiple ranges separated by a + sign. For instance {THROUGHPUT:0-10+50-100}. One can also control the ratio between one part and the other by setting a third number after the range: {THROUGHPUT:0-10-20+0-30-100-80} will create a plot where the first range is 20% and the second 80% of the total axis.
- **var_format** ={THROUGHPUT:%dGbps} Printf like formating of va And the prefix should be changed.riables. Eg this example will display all visualisation of the value of throughput (eg in the axis) as XGbps. Use in combination to var_divider.  You can also pass `eng` to have an engineering formatting (e.g. 1 k, 2 M, ...). Optionally, `eng.2` will print engineering format with 2 decimal places, while `eng.2.Hz` will print e.g. `2.44 kHz`.
- **var_ticks**, {THROUGHPUT:0+5+10+15+20} Define where the ticks should be set, in this example there will be ticks in 0,5,...20.
- **graph_tick_params** ={direction:in} Arguments given to matplotlib's `tick_params()`.
- **graph_x_sort** =true/false, or a list of variables: sort the values of the X axis. By default only numerical variables are sorted.
- **graph_show_xlabel**, **graph_show_ylabel** =true/false, or a list of results: show the label of the X or Y axis. Default true.

Units and name of variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **var_names**, {"result-LATENCY":"Latency (µs)","result-THROUGHPUT":"Throughput"})
- **var_unit**, {"result": "bps","result-LATENCY":"us","latency":"us","throughput":"bps"})

Plot types
^^^^^^^^^^

- **graph_type** =type, or {RESULT:type} Force the type of graph: `line`, `bar`, `simple_bar`, `barh` (horizontal bars), `boxplot`, `cdf` (see `CDF`_), `heatmap` or `sparse_heatmap`. A list gives the type of each subplot.
- **graph_only** ={THROUGHPUT,LATENCY} Only draw the graphs of these results.
- **graph_scatter** =true/false Use a scatter plot instead of a lineplot, default false. You must arrange the data so it displays as a line plot (one dynamic variable only).
- **var_grid** ={result} Results and variables that have a grid: by default all the results. `var_grid=false` removes it. Also written **graph_grid**.
- **graph_grid_linestyle** =: Line style of the grid.
- **graph_bar_stack** =true/false If your series are a complex barplot (more than 1 dynamic variable), it will stack the plots instead of adding them one after the other. Default is false.
- **graph_bar_hatch** =true/false Hatch the bars, with a pattern per series. Default false.
- **graph_bar_inter** =0.1 Space between the groups of bars. By default 0.1, or 0.05 with more than 20 bars.
- **graph_x_label** =true/false In bar plots, show the label of each group of bars. Default true.
- **graph_show_fliers** =true/false In box plots, show the outliers. Default true.
- **graph_smooth** =N Smooth the lines over N% of the X axis. Default 1, no smoothing.

Time series and namespaces
^^^^^^^^^^^^^^^^^^^^^^^^^^
When handling time series (see :ref:`namespace`), you might want to synchronize or shift the time for some time series namespaces. Contrary to the options provided in the :ref:`namespace` page, these options do not affect the data recorded in the database but only the graph.

- **var_sync** = list["time"] Synchronize multiple time series on the X axis, shifting them by the first value.
- **var_shift** = dict[metric:shift,...] Shift all given metric by the given values. Useful to resynchronize time, though the best practice is to do it upfront.
- **var_repeat** = list[metric] Ensure all given metrics have datapoints at the same value, repeating them from the previous value if necessary.

Series tweaking
^^^^^^^^^^^^^^^

- **graph_series_sort** =method Sort series according to the method wich can be : "natsort", natural alphabetical sorting, "avg", "min" or "max" to sort according "y" values. The sorting can be inversed by prefix the method with "-". Default is to not reorder.
- **graph_max_series** =N limint the number of series to N, used in conjunction with graph_series_sort to only show the "best" series. By default there is no limit.
- **var_serie** =variable Use a specified variable as the serie of a line plot. Also written **graph_serie**.
- **graph_max_variables** =3 When there are more dynamic variables, NPF removes the least useful ones.
- **graph_keep_variables** ={A,B} Variables that ``graph_max_variables`` must not remove (also ``--graph-keep-variables``).

Information on graphs
^^^^^^^^^^^^^^^^^^^^^
- **title** =title Title of the graph
- **var_hide** ={A,B,...} List of variables to hide
- **graph_label_dir** (or **var_label_dir**) ={A:vertical,B:horizontal} Force the direction of labels on the X axis for the given variables. By default, vertical when there are more than 8 values, horizontal otherwise. Accepted values: vertical, horizontal, diagonal
- **graph_force_diagonal_labels** =true/false Always use diagonal labels for the X axis, independently from the `var_label_dir` setting. False by default.
- **graph_show_values** =N Write the values on the graph, with N decimals.
- **graph_background** =N, or {RESULT:N} Background color of the graph, an index in the color list. `true` uses 15.
- **graph_labels** ={A,B} Labels of the series in the legend, in order, instead of their names.
- **graph_series_label** =text Name of the series, where the variables are replaced, e.g. `$CPU cores`.
- **graph_variables_explicit** =true/false Name the series made from a variable "VAR = value" instead of "value". Default false.
- **graph_hide_variables** ={A,B} Remove these variables from the graphs and outputs, as if they were not dynamic.

Legend
^^^^^^
- **graph_legend** =true/false Enable/disable legend. Default is true.
- **legend_loc** (or **graph_legend_loc**) =best Legend location, using matplotlib terminology (see `legend <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html>`_), eventually prefixed by `outer` to put the legend outside the graph. E.g. `outer lower center`
- **legend_ncol** (or **graph_legend_ncol**) =1 Number of columns in the legend. A list gives it per subplot.
- **legend_frameon** =true/false Draw a frame around the legend. Default true.
- **legend_bbox** ={0,1,1,.05} Where an outer legend goes (matplotlib's `bbox_to_anchor`).
- **legend_mode** =expand Matplotlib's `mode` of the legend.
- **subplot_legend_loc** ={upper left,lower right} With a dual-axis plot (`graph_subplot_type=axis`), the location of the legend of each axis.
- **graph_subplot_unique_legend** =true/false With a dual-axis plot, a single legend for all the axes. Default false.
- **graph_legend_params** ={} Dictionnary of arguments to pass to matplotlib legend() function, e.g. `{frameon:0,facecolor:black}`

Data transformation
^^^^^^^^^^^^^^^^^^^

- **graph_combine_variables** (or **var_combine**) ={NUMA+CORE:SCORE} will combine multiple variables in a single one. Eg if you have a NUMA={0,1} variable, and CORE=[1-4] this will combine them as a single variable SCORE={0-1,0-2,0-3,0-4,1-1,1-2,1-3,1-4}. This allows to reduce the number of variables to graph, eg you may prefer to have a lineplot of SCORE, instead of a barplot of NUMA and CORE according to the serie.
- **graph_series_as_variables** =true/false Will convert the series as a variable. This is useful in npf-compare to consider the different tags/software you used as a variable, and use something else as a serie.
- **graph_variables_as_series** ={VAR1,VAR2} list of variables to use as series. If multiple, or a serie already exists, it will do the cross product of the variables. Usefull to pass "trailing" dynamic variables as more lines in a lineplot.
- **graph_result_as_variable** (or **result_as_variables**) ={COUNT-Q(.*):QUEUE-COUNT} Group multiple results matching a regex as a single variable. Eg if you run a single test that outputs multiple statistics for "the same thing", like the number of bytes per NIC queues, you will have your scipt display RESULT-COUNT-Q0 A, RESULT-COUNT-Q1 B,  ... and this example will make a variable QUEUE with all the observed values, and create a new result type called "COUNT".
- **var_divider**, {'result':1} Divide the variables or results by the given value.
- **var_round** ={VARIABLE:precision} Round the values of a variable, merging the runs that become equal.
- **graph_filter** ={RESULT:x<1000} Keep only the values `x` of a result for which the expression is true.
- **graph_map** ={VARIABLE:file} Replace the values of a variable with the map in a file, made of `regex:value` lines (several files separated by +). Useful with text results. It is a reduced of what the `perf-class <https://pypi.org/project/perf-class/>`_ project proposes.
- **graph_map_inline** ={regex:value} Replace the values of all variables that match a regex by another.
- **graph_series_prop** =true/false Divide all results by the results of the first serie. Hence graphs will be a percentage of relative to the first series. Eg if the first serie is "software 1" it will be removed from the graph and the other series will show how much better software 2, ... did against software 1. Alternative value : =integer, e.g. =100 shortcut to multiply the result by the given value to have a proportion in, e.g. percents.
- **graph_cross_reference**, {Y:VARIABLE}, change the graph where the Y axis is Y (the result name) to have the X variable being another variable. Typically used to replace a generator rate on the X axis by the actual throughput.
- **var_aggregate**, {VARIABLE:method}, aggregates all values for a given variable. If "method" is "all", all results will be put in a single variable value like if they were all points for the same run. You can also use "median", "average", ... to combine results for all variables using those mathematical methods. See :ref:`aggregate` for an example.
  

Graph filtering
^^^^^^^^^^^^^^^
- **graph_filter_by** = {variable:filter} In a lineplot, changes a line by a dashed-line according to a filter. For instance `graph_filter_by={THROUGHPUT:DROPPEDPC<10}`
- **graph_filter_linestyle** =-- and **graph_filter_fillstyle** =none Line style and marker fill style of the filtered parts.

.. collapse:: Example
   :class: collapse

   Data:

   +---------+----------------+-------------+
   |         | **Throughput** | **Dropped** |
   +=========+================+=============+
   | **10**  | 10.0           | 0.0         |
   +---------+----------------+-------------+
   | **20**  | 20.0           | 0.0         |
   +---------+----------------+-------------+
   | **30**  | 30.0           | 0.0         |
   +---------+----------------+-------------+
   | **40**  | 40.0           | 0.0         |
   +---------+----------------+-------------+
   | **50**  | 50.0           | 0.0         |
   +---------+----------------+-------------+
   | **60**  | 57.0           | 5.0         |
   +---------+----------------+-------------+
   | **70**  | 63.0           | 10.0        |
   +---------+----------------+-------------+
   | **80**  | 68.0           | 15.0        |
   +---------+----------------+-------------+
   | **90**  | 72.0           | 20.0        |
   +---------+----------------+-------------+
   | **100** | 75.0           | 25.0        |
   +---------+----------------+-------------+

   Will give the following graphs that underlines that a certain part of the throughput graph is representing values that include packets being dropped. It conveys to the reader that while that line achieves a higher throughput, dropping packets is unnacceptable in most conditions.

   .. image:: https://github.com/tbarbette/npf/blob/main/doc/filter-THROUGHPUT.png?raw=true
      :alt: Example of graph with graph_filter_by
      :width: 500

   The NPF script example is available `in integration/filter.npf <https://github.com/tbarbette/npf/blob/main/integration/filter.npf>`_.



Splitting graphs in sub-plots
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **graph_subplot_results** ={THROUGHPUT+LATENCY:2} combine two results in a single figure. If graph_subplot_type is subplot, then it will simply combine the graphs in a single file using the given number of columns. If the subplot_type is axis, it will use a dual-axis plot. Only the last variable will be on the second axis, so one may combine multiple variables on the same axis, like TX and RX throughput on the left axis, and the latency on the right axis?
- **graph_subplot_variable** =X will make one sub-plot for every value of the variable X. In general this is to be used with `graph_variables_as_series` to explode one other variable as serie and display more dimensions. Use `graph_max_cols` to limit the number of columns. E.g. to have vertical subplots set `graph_max_cols=1`.
- **graph_display_statics** =true/false Will add a subplot to show the value of static variables. Useful to exchange graphs with colleages knowing what are the fixed parameters for all the graph you show. But the results is somehow horrible.
- **graph_text** =string Add some texts under all graphs.
- **graph_subplot_type** =subplot With `graph_subplot_results`, `subplot` draws one subplot per result, and `axis` one Y axis per result in a single plot.
- **graph_max_cols** =2 Maximum number of columns of subplots.

Aliases
^^^^^^^

Some options have other names: graph_grid is var_grid, graph_ticks is var_ticks, graph_serie is var_serie, graph_types is graph_type, graph_linestyle is graph_lines, var_combine is graph_combine_variables, series_as_variables is graph_series_as_variables, var_as_series, graph_variable_as_series, graph_variable_as_serie and graph_variables_as_serie are graph_variables_as_series, result_as_variables is graph_result_as_variable, y_group is graph_y_group, graph_serie_sort is graph_series_sort, series_prop is graph_series_prop, graph_legend_ncol is legend_ncol, graph_legend_loc is legend_loc, graph_do_legend and do_legend are graph_legend, var_label_dir is graph_label_dir, graph_subplot_variables is graph_subplot_variable and graph_max_col is graph_max_cols.
NPF also accepts an option with or without a final s, e.g. graph_variable_as_series.
