.. _tests:

*************************
Writing a NPF test script
*************************

Sections
========

A NPF test script is made of sections. There are several types of sections.
In a test script, a section starts with a header identified by a ``%`` sign prefixing its type name.
For instance ``%info`` is starts an info section.
A section can take arguments, separated by spaces and following its type name.

``%info``
    Contains information about what the test script does. The first line is used as graph title by default.
``%config``
    Configuration options for the test execution and graph styling.
``%variables``
    List of variables to define the matrix of parameters to test.
``%late_variables``
    List of variables that are not to be considered part of the test, like constants.
``%script``
    Bash commands to execute for the test. Can be defined to run with a specific role when appended with ``@rolename``.
``%init``
    Special script run once before all other scripts.
``%import``
    Import another test script and optionally under a given role when appended with ``@rolename``. 
    NPF comes with *modules* test scripts intended for importation. They usually do specific tasks that can be re-used such as setting the CPU frequency.
``%include``
    A test script to be included inline. It can be used to organise a test script in multiple files.
``%sendfile``
    Send a file that lies with the test script to the remote machine. The source path of the file is given as first argument. The destination path is the test execution directory.
``%require``
    Determines whether the test can run. NPF runs a test when all lines of the section returns a zero return code.
``%pyexit``
    A Python script executed after the test. It can change and interpret its results.
``%file``
    Creates a file with the filename given as first argument. The content of the file is the section content.

The following subsections describes NPF script sections in more details.

Script
------

The script section is the heart of NPF. A script section defines a series
of bash commands to be executed.

.. code-block:: bash

    %script
    TOTAL=$(bc 5 + 3)
    echo "RESULT $TOTAL"

This script executes locally those two commands, and
stores the result by using the ``echo "RESULT value"`` construct.

.. By default a test is executed 3 times to observe the variance.

There can be multiple ``RESULT``:

.. code-block:: bash

    %script
    ADD=$(bc 5 + 3)
    DIFF=$(bc 5 - 3)
    echo "RESULT-ADDITION $ADD"
    echo "RESULT-DIFFERENCE $DIFF"

The two results are stored and two graphs are produced, showing that the
value of ``ADDITION`` is 8 and the ``DIFFERENCE`` is 2.

Finally, scripts sections can specify a role which wil execute their code,
and arguments regarding their execution.

.. code-block:: bash

    %script@client delay=5 autokill=false
    echo "EVENT finished"

    %script@server waitfor=finished sudo=true
    echo "RESULT 79"

In this example, the first script is executed on the ``client`` role while the
second is executed on the ``server`` role. Roles are abstract identities that are
associated at run time to real computers in the cluster, either by specifying cluster nodes
files as described in section :ref:`cluster` or by using the command line argument
``--cluster role1=address1 [role2=address2 [...]]``.

This example also specifies additional arguments.
The first script starts 5 seconds after the test execution has begun (``delay=5``), and its completion does not halt the test execution (``autokill=false``). 
The second script is executed when the ``finished`` event is reached (``waitfor=finished``) and with elevated priviledges (``sudo=true``).

Handling multiple results
~~~~~~~~~~~~~~~~~~~~~~~~~
NPF extracts all results prefixed by ``RESULT[-VARNAME]``.

If there are multiple occurences of the same `VARNAME`, NPF will by default overwrite values and keep only the last one.

There are 2 other possible actions: appending the results as a list of possible values, or directly summing all values.

When ``VARNAME``
is in the list ``result_add={VARNAME,...}`` given either in the `%config` section or `--config` parameter, values will
be summed together.
If `VARNAME`` is in the ``result_append={VARNAME,...}`` config list, results
will be append as a list.
In a plot, all values will be used to show a standard deviation.

Let's follow this sample output of an experiment:

.. code-block::

    RESULT-THROUGHPUT 6
    RESULT-THROUGHPUT 10
    RESULT-THROUGHPUT 26

Here's the result for all possible modes:

.. tabs::

   .. tab:: Default

      .. image:: https://github.com/tbarbette/npf/raw/master/doc/example_multiple_result_default-THROUGHPUT.png?raw=true
         :width: 500

   .. tab:: Add

      .. image:: https://github.com/tbarbette/npf/raw/master/doc/example_multiple_result_add-THROUGHPUT.png?raw=true
         :width: 500

   .. tab:: Append

      .. image:: https://github.com/tbarbette/npf/raw/master/doc/example_multiple_result_append-THROUGHPUT.png?raw=true
         :width: 500

.. _namespaces:

Namespaces
~~~~~~~~~~

A single run of a single experiment might produce a series of values.
Typically, the throughput over time for the duration of the whole experiment.


Consider the following output of an experiment:

.. code-block::

    TIME-1001-RESULT-THROUGHPUT 7 pps
    TIME-1002-RESULT-THROUGHPUT 8 pps
    TIME-1003-RESULT-THROUGHPUT 9 pps
    TIME-1004-RESULT-THROUGHPUT 6 pps
    RESULT-RX 30
    RESULT-TX 28

In that experiment, there was 30 packets received and 28 sent.
However the operator also exported the throughput in `pps` every second.
RX and TX are single value for the whole experiment's run. But there are 4 values for the THROUGHPUT that must stay associated with their TIME.

.. tabs::

   .. tab:: Throughput

      .. image:: https://github.com/tbarbette/npf/raw/master/doc/example_namespaces-THROUGHPUT.svg?raw=true
         :width: 500

   .. tab:: Throughput (synced)

      With ``--config var_synced={time}`` to synchronize the values upon the first one (note the X axis)

      .. image:: https://github.com/tbarbette/npf/raw/master/doc/example_namespaces_synced-THROUGHPUT.svg?raw=true
         :width: 500



The use of namespace is not restricted to time. For instance one might want to extract the number of packets received per CPU cores using a format like `CPU-XXX-RESULT-NBPACKETS YYY`.
This will automatically create an histogram of the number of packets per core for the experiment.


Variables
---------

The ``%variables`` section defines variables and the values they can take.
NPF generates executions of a test scripts to explore the combinations of values these variables can take.
Values of a variable named ``LENGTH`` can be retrieved with patterns ``$LENGTH`` or ``${LENGTH}`` in ``%script`` and ``%file`` sections of a test file.

.. code-block:: bash

    %variables
    NUMBER=[1-10]

    %script
    ADD=$(echo "$NUMBER + $NUMBER" | bc)
    MULT=$(echo "$NUMBER * $NUMBER" | bc)
    echo "RESULT-ADDITION $ADD"
    echo "RESULT-MULT $MULT"

NPF executes this test script by running the script sections for all values of ``$NUMBER``, i.e. from 1 to 10.
More details on variables can be found in the :ref:`variables` page.

Late variables
~~~~~~~~~~~~~~

The ``%late_variables`` section defines constants variables.
Their values remain identical throughout the execution of the test.
These variables are omitted from graphs.

.. code-block:: bash

    %variables
    RADIUS=[1-10]

    %late_variables
    PI=3.14

    %script
    MULT=$(echo "$RADIUS * $PI * $PI" | bc)
    echo "RESULT-SURFACE $MULT"

This examples computes the surface of a circle, with the ``PI`` variable given as constant.
The ``SURFACE`` result is plotted against the ``RADIUS`` variable, without showing the ``PI`` constant.

Tags
~~~~

``%script`` sections and variables can be omitted or included base on a tag, given by a ``repo`` or the ``--tags tag [tag ...]`` argument.

.. code-block:: bash

    %variables
    NUMBER=[1-10]
    CPU=1
    cpu:CPU={0,1}

When the ``cpu`` tag is given, ``$CPU`` take values 0 and 1. Otherwise, ``$CPU`` takes the value 1.
Tags allow to toggle in and out variables and script sections together. This can be used to test more values and more features when needed.

``npf-compare`` can also be given repositories with a tag, e.g. ``npf-compare "iperf+feature:IPerf with the feature tag" "iperf:CPU=8:IPerf with 8 CPU" --test ...``

Config
------

The ``%config`` section contains configuration options, both related to the execution of the test and the graphs format.
All graph-related configuration options are described in the :ref:`graphs page<graph>`.

``acceptable=0.01``
    Acceptable difference between multiple regression runs 
``n_runs=1``
    Number of runs to do of each test
``unacceptable_n_runs=0``
    Number of runs to do when the value is first rejected (to avoid false positives). 
    Half the most abnormal runs will be rejected to have a most common value average.
``required_tags=``
    Comma-separated list of tags required to run the test

Include
-------

The ``%include`` section allows including a file inline in the test.
Using this section, a complex NPF test file can be split in multiple files.
Parameters of the included file can be overwritten by passing ``VAR=VAL`` pairs as arguments.

.. code-block:: bash

    surface.npf:

    %script
    MULT=$(echo "$RADIUS * $PI * $PI" | bc)
    echo "RESULT-SURFACE $MULT"


    test.npf:

    %variables
    RADIUS=[1-10]

    %include surface.npf PI=3.14

    
The value of ``PI`` is overwritten when including the ``surface.npf`` script.

Import
------

The ``%import`` section is used to import *modules*.
Modules are small scripts that can be re-used in NPF scripts. Modules cannot specify roles.
Rather, when importing a module, its role is specified using the ``%import@role`` construct.
These modules can be a packet generator, a module to measure the bitrate of a device, etc. 
Modules reside in the ``modules`` folder.

.. code-block:: bash

    modules/clock.npf:
    
    %script
    for i in seq($MAX_CLOCK) ;
    do
        echo "$(hostname)-$i-RESULT-CLOCK $i"
        sleep 1
    done

    test.npf:

    %variables
    MAX_CLOCK=30

    %import@client clock
    %import@server clock   

In this example, a ``clock.npf`` module is defined and imported for the ``server`` and ``client`` roles.

pyexit
------

A python script can be executed after each test runs.

One can use the %pyexit section to transform the results:

.. code-block:: python

    %pyexit
    import numpy as np
    loss=RESULTS["RX"] - RESULTS["TX"]
    RESULTS["LOSS"]=loss

This can be used to compute some intermediate results, compute variance among
multiple results, etc.
Two dictionnaries are exposed to access the results of the experiment.
As in the example above, `RESULTS` allow to access single-value results from the experiment. For instance, a valid output for the sample above could be:

.. code-block::

    RESULT-RX 800
    RESULT-TX 1000

In a CSV or a graph, the new `LOSS` result will be shown/drown.

:ref:`namespaces` results are available under ``KIND_RESULTS``.
It is a dictionnary of the namespace as key, and a dictionnary including a result in the format presented above for each iteration of the variable in the namespace.

Here's an example to take all values over time of a namespace.
Typically a throughput is shown
every second with a series of results like `TIME-YYY-RESULT-THROUGHPUT XXX`, with `YYY` being an increasing time and XXX the throughput at value.

For a result such as:

.. code-block::

    TIME-1-RESULT-THROUGHPUT 7
    TIME-2-RESULT-THROUGHPUT 8
    TIME-3-RESULT-THROUGHPUT 9
    TIME-4-RESULT-THROUGHPUT 6

The dictionnary will be:

.. code-block::

    KIND_RESULTS
    {
        'TIME' : {
            1:  {
                'THROUGHPUT': [7]
            },
            2:  {
                'THROUGHPUT': [8]
            },
            3:  {
                'THROUGHPUT': [9]
            },
            :  {
                'THROUGHPUT': [6]
            }
        }
    }

The following code will
create a combination of all values as `THROUGHPUT-SUM`, that can then be used in a boxplot.

.. code-block:: python

    %pyexit

    for kind,results in KIND_RESULTS.items():
        d={}
        for time, kv in results.items():
            for k,v in kv.items():
                d.setdefault(k,[])
                d[k].append(v)
        for k,vs in d.items():
            RESULTS[k + '-SUM'] = vs[8:-1]


NPF constants
=============

Multiple constants can be used in the files and scripts sections: 

``NPF_ROOT``
    Path to NPF (path to the executable)
``NPF_BUILD_PATH``
    Path to the build folder of NPF (by default $NPF_ROOT/build, can be overriden with ``--build-path``)
``NPF_REPO``
    Path to the repository under test. If you don't use a repository, it will be the cwdir of the executable.
``NPF_TESTSCRIPT_PATH``
    Path to the folder containing the test script
``NPF_RESULT_PATH``
    Path to the result folder (by default ``results/repo/version/``, or as overwritten by `--result-path`` option)
``NPF_OUTPUT_PATH``
    Path to the output folder (by default the same as the result result, unless given with `--output-filename`)
``NPF_NODE_ID``
    Index of the node used for the same role, in general 1
``NPF_NODE_MAX``
    Number of nodes running the same role, in general 1
``NPF_MULTI_ID``
    Index of the script when running multiple times the same script on each node using the "multi" feature to run multiple time the same script on each role (see :ref:`multi`), in general 1
``NPF_MULTI_MAX``
    Number of multi as given to the cluster config (default is 1)

Test scripts shipped with NPF
=============================

Generic
-------

Generic tests are used to do black-box testing, they are L2/L3
generators, packets trace replayers and HTTP generators.

They are generic in the sense that they can be used to
test any device under test in the middle of a client and a server.

-   generic\_dpdk : DPDK-based tests, need a DPDK environment setted up
-   generic : Other tests using the normal OS stack

TODO : expand this section