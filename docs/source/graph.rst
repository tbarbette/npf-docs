Graph are automatically generated for all tested variables
combinations.

To choose the type of graph, the number of dynamic variables (I.e. variables that have more than one values) is taken into account, along with the number of series.

For instance, if there is only one dynamic variable, a line plot will be used, with one line per series. If there is no dynamic variables, a barplot will be used, but a box plot can also be used.


Below, npf-run gave two series to the grapher (current and last commit), while the test script
generate a matrix of Burst and Lengths, that is 2 dynamic variables and only a barplot can render that correctly
as lines would be uncomparable.

.. image:: https://github.com/tbarbette/npf/raw/master/doc/sample_graph.png
   :width: 400
   :alt: Sample graph

If there are 2 dynamic variables, but only a single serie (i.e. you used npf-compare with a single serie, or npf-run with --history 0), one of the variable will be taken out as serie, and a line plot will still be used:

.. image:: https://github.com/tbarbette/npf/raw/master/doc/sample_graph3.png
   :width: 400
   :alt: Sample graph

One can force the graph type with the "graph_type" config option. For instance, if you pass "--config graph_type=boxplot" to the command line, you will get a box plot no matter the number of dynamic variables.

#### Graphing options
The graph can be tweaked using many options, and the data can also be transformed using multiple tools to better display results. Data transformation will also affect the output CSV. In any case none of these options affect the values in the data cache, so you may try different tweaks without risks.

All the following options can be added to the %config section of the test script, or after the --config parameter on the command line of any of the tools.

This section is in rework.
 * var prefix generally affect variables. It generally takes a list of variables, or a dict of variables->parameters.
 * graph prefix only affect the graph, styling ,etc. The CSV data will not be changed.

##### Graph styling
###### Confidence intervals
 * **graph_error_fill**=true/false Display a "filling zone" instead of error bars. To be used when you have many points and your graph becomes horrible.
###### Line/series style
 * **graph_color**={0,1,2,3} Select a set of color for each serie. Colors are predefined ranges. Default is to use the 0 set of colors for all series, the serie 0 is a mix of different colors, while 1 to 5 are shades of the same colors.
 * **graph_markers**={'o', '^', 's', 'D', '*', 'x', '.', '_', 'H', '>', '<', 'v', 'd'}, type of markers to be used, per-serie. Default if this. See matplotlib docs to find the type.
 * **graph_lines**={'-', '--', '-.', ':'} Type of lines, per-series.
###### Scaling and axis limits
 * **var_log**, [THROUGHPUT,LATENCY] Define variables that should be shown in a log axis in base 2
 * **var_log_base**, {THROUGHPUT:2} Define variables that should be shown in a log axis, with the specified base (default is 2 with var_log)
 * **var_lim**, {THROUGHPUT:0-100} Define the range for some variables, useful to cap graphs. One can produce "broken axis" graphes by giving multiple ranges separated by a + sign. For instance {THROUGHPUT:0-10+50-100}. One can also control the ratio between one part and the other by setting a third number after the range: {THROUGHPUT:0-10-20+0-30-100-80} will create a plot where the first range is 20% and the second 80% of the total axis.
 * **var_format**={THROUGHPUT:%dGbps} Printf like formating of va And the prefix should be changed.riables. Eg this example will display all visualisation of the value of throughput (eg in the axis) as XGbps. Use in combination to var_divider.
  * You can also pass `eng` to have an engineering formatting (e.g. 1 k, 2 M, ...).
    Optionally, `eng.2` will print engineering format with 2 decimal places, while `eng.2.Hz` will print e.g. `2.44 kHz`.
 * **var_ticks**, {THROUGHPUT:0+5+10+15+20} Define where the ticks should be set, in this example there will be ticks in 0,5,...20.

###### Units and name of variables
 * **var_names**, {"result-LATENCY":"Latency (µs)","result-THROUGHPUT":"Throughput"})
 * **var_unit**, {"result": "bps","result-LATENCY":"us","latency":"us","throughput":"bps"})

###### Plot types
 * **graph_scatter**=true/false Use a scatter plot instead of a lineplot, default false. You must arrange the data so it displays as a line plot (one dynamic variable only).
 * **graph_grid**=true/false Display a grid on the graph. Default false.
 * **graph_bar_stacks**=true/false If your series are a complex barplot (more than 1 dynamic variable), it will stack the plots instead of adding them one after the other. Default is false.
###### Series tweaking
 * **graph_series_sort**=method Sort series according to the method wich can be : "natsort", natural alphabetical sorting, "avg", "min" or "max" to sort according "y" values. The sorting can be inversed by prefix the method with "-". Default is to not reorder.
 * **graph_max_series**=N limint the number of series to N, used in conjunction with graph_series_sort to only show the "best" series. By default there is no limit.
 * **graph_serie**=variable Use a specified variable as the serie of a line plot.
###### Information on graphs
 * **graph_legend**=true/false Enable/disable legend. Default is true.
 * **title**=title Title of the graph
 * **var_hide**={A,B,...} List of variables to hide
 * **var_label_dir**={A:vertical,B:horizontal} Force the direction of labels on the X axis for the given variables. By default, vertical when there are more than 8 values, horizontal otherwise. Accepted values: vertical, horizontal, diagonal
 * **graph_force_diagonal_labels**=true/false Always use diagonal labels for the X axis, independently from the `var_label_dir` setting. False by default.

##### Data transformation
 * **var_combine**={NUMA+CORE:SCORE} will combine multiple variables in a single one. Eg if you have a NUMA={0,1} variable, and CORE=[1-4] this will combine them as a single variable SCORE={0-1,0-2,0-3,0-4,1-1,1-2,1-3,1-4}. This allows to reduce the number of variables to graph, eg you may prefer to have a lineplot of SCORE, instead of a barplot of NUMA and CORE according to the serie.
 * **series_as_variables**=true/false Will convert the series as a variable. This is useful in npf-compare to consider the different tags/software you used as a variable, and use something else as a serie.
 * **var_as_series**={VAR1,VAR2} list of variables to use as series. If multiple, or a serie already exists, it will do the cross product of the variables. Usefull to pass "trailing" dynamic variables as more lines in a lineplot.
 * **result_as_variables**={COUNT-Q(.*):QUEUE-COUNT} Group multiple results matching a regex as a single variable. Eg if you run a single test that outputs multiple statistics for "the same thing", like the number of bytes per NIC queues, you will have your scipt display RESULT-COUNT-Q0 A, RESULT-COUNT-Q1 B,  ... and this example will make a variable QUEUE with all the observed values, and create a new result type called "COUNT".
 * **var_divider**, {'result':1}) Divide the variables or results by the given value.
 * **graph_map**={regex:value} Replace a value matching a regex by another. Useful with text results. It is a reduced of what the `perf-class <https://pypi.org/project/perf-class/>` project proposes.
 * **graph_series_prop**=true/false Divide all results by the results of the first serie. Hence graphs will be a percentage of relative to the first series. Eg if the first serie is "software 1" it will be removed from the graph and the other series will show how much better software 2, ... did against software 1. Alternative value : =integer, e.g. =100 shortcut to multiply the result by the given value to have a proportion in, e.g. percents.
 * **graph_cross_reference**, {Y:VARIABLE}, change the graph where the Y axis is Y (the result name) to have the X variable being another variable
 * **var_aggregate**, {VARIABLE:method}, aggregates all values for a given variable. If "method" is "all", all results will be put in a single variable value like if they were all points for the same run. You can also use "median", "average", ... to combine results for all variables using those mathematical methods.

##### Combining graphs (subplots)
 * **graph_subplot_results**={THROUGHPUT+LATENCY:2} combine two results in a single figure. If graph_subplot_type is subplot, then it will simply combine the graphs in a single file using the given number of columns. If the subplot_type is axis, it will use a dual-axis plot. Only the last variable will be on the second axis, so one may combine multiple variables on the same axis, like TX and RX throughput on the left axis, and the latency on the right axis?
 * **graph_display_statics**=true/false Will add a subplot to show the value of static variables. Useful to exchange graphs with colleages knowing what are the fixed parameters for all the graph you show. But the results is somehow horrible.
 * **graph_text**=string Add some texts under all graphs.

