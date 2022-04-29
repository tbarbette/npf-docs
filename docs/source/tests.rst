.. _tests:

****************************
Writing a *.npf* test script
****************************

Sections
========

The test script is made of multiple sections, starting with a `%` sign like
`%file CONFIG` which means that a file named CONFIG should be created
with the content following the section header.

List of sections : 
    * info : Information about what the test script does. Usually the first line is the title and will be by default used as the graph title 
    * config : Configuration options. See below.
    * variables : List of variables to define the matrix of parameters to try
    * late_variables: List of variables that are not to be considered part of the test, like constants.
    * script : Bash commands to execute, the heart of the test. Can be defined to run with a specific role, role are mapped to cluster nodes. See the cluster section below 
    * init : Special script that run only once, before all other scripts (therefore, can be fought as an initialization script)
    * import : Import another test script and optionally under a given role. The repository comes with some "modules" test scripts intended for importation. They usually do specific tasks that we don't want to rewrite in all test script such as setting the cpu frequency, IP addresses for some NICs, ...
    * include : A test script to be included inline, not as a sub-test script like import but merely to be considered as a way to organise your test script in multiple files
    * sendfile : Send a file that lies with the test script to the remote machine
    * require : A special script that tells if the test script can run. If any line produce a return code different than 0, the test script will not run
    * pyexit : A python script that will be executed after each tests (but only once after all runs), mainly to change or interpret the results

Script
------

The script is the heart of NPF. A script section defines a simple list
of bash commands to be executed.

.. code-block:: bash

    %script
    TOTAL=$(bc 5 + 3)
    echo "RESULT $TOTAL"

This simple test script will execute locally those two commands, and
"collect" the result that is 8. By default a script is re-executed 3
times to observe the variance.

There can be multiple RESULT:

.. code-block:: bash

    %script
    ADD=$(bc 5 + 3)
    DIFF=$(bc 5 - 3)
    echo "RESULT-ADDITION $ADD"
    echo "RESULT-DIFFERENCE $DIFF"

The result will be collected, and 2 graphs will be produced, showing the
value of ADDITION is 8 and the DIFFERENCE is 2.

Finally, scripts can take some parameters and can be required to be
executed on a specific machine (roles):

.. code-block:: bash

    %script@client autokill=false delay=5
    echo "EVENT finished"

    %script@server sudo=true waitfor=finished
    echo "RESULT 79"

In this example, the first script will be launched on "client" and the
second on "server". See :ref:`cluster` to check how to attribute those
roles to real machines. The first script will not interrupt the test
when it finishes, and will start after a delay of 5 seconds. The second
script will run on "server", with elevated priviledges. But it will run
only when the first one has finished and displayed the "finished" event.

Variables
---------

List of variables that will be replaced in any script or file section
(searching for pattern $VARIABLE or ${VARIABLE}).

.. code-block:: bash

    %variables
    NUMBER=[1-10]

    %script
    ADD=$(echo "$NUMBER + $NUMBER" | bc)
    MULT=$(echo "$NUMBER * $NUMBER" | bc)
    echo "RESULT-ADDITION $ADD"
    echo "RESULT-MULT $MULT"

The example above will re-execute the test (script) for all "NUMBER"
from 1 to 10. The following graphs will be automatically produced:
![sample
picture](examples/tests-readme-ADDITION.png "Result for ADDITION")![sample
picture](examples/tests-readme-MULT.png "Result for MULT"). See the :ref:`graphing page<graph>` to style the graph and
change units, axis names, etc...

Late variables
~~~~~~~~~~~~~~
For every run of every combination of variables, %late_variables defines a serie of supplementary parameters to consider. Those parameters cannot be list, they must all be constant.
This is interesting to define constant of the experiment, parameters that will not polute the "X" of your dataset.

.. code-block:: bash

    %variables
    RADIUS=[1-10]

    %late_variables
    PI=3.14

    %script
    MULT=$(echo "$RADIUS * $PI * $PI" | bc)
    echo "RESULT-SURFACE $MULT"


Tags
~~~~

Variables can optionaly be prefixed with a tag and a colon to be
included only if a tag is given. In the following example:

.. code-block:: bash

    %variables
    NUMBER=[1-10]
    CPU=1
    cpu:CPU={0,1}
    
If the *cpu* tag is given, `$CPU` will be expanded by 0 and 1 `--cpu:CPU=1`.  If the tag cpu is not given, `$CPU`
will be expanded by 1.

This allows to do more extanded tests to grid-search some value, but do not include that in most tests.

All variables types and discussion about experimental design can be found in :ref:`the variables page <variables:variables>`.

There are 3 ways to specify a tag:

* by the repository in the `.repo` file (see :ref:`the reositories page <repos>`)
* by the command line argument ``\-\-tags TAG``
* with npf-compare, by duplicating a repository and specifying a list of tags or overwritten variables, e.g. ``npf-compare "iperf+feature:IPerf with the feature tag" "iperf:CPU=8:IPerf with 8 CPU" --test ...``

Config
------

List of test configuration option not related to graphing (those ones
are described :ref:`graphing page<graph>`):

* acceptable=0.01 Acceptable difference between multiple regression runs 
* n\_runs=1 Number of runs to do of each test
* unacceptable\_n\_runs=0 Number of runs to do when the value is first rejected (to avoid false positives). Half the most abnormal runs will be rejected to have a most common value average.
* required\_tags= Comma-separated list of tags needed to run this run

Include
-------
An include allows to import a sub-file as if its content was part of the your script. You can also overwrite parameter as PI in the following example.

.. code-block:: bash
    test.npf:

    %variables
    RADIUS=[1-10]

    %include surface.npf PI=3.14

    surface.npf:
    %script
    MULT=$(echo "$RADIUS * $PI * $PI" | bc)
    echo "RESULT-SURFACE $MULT"

If PI was set in %variables, the test would run for "RADIUS=1 PI=3.14", then "RADIUS=2 PI=3.14", ... It's better to keep it out of the list of variables, even if technically, it works.

Import
------

Imports are much like includes, except they're meant to be re-used in different NPF scripts. For instance a packet generator, a module to measure the bitrate of a device, etc. Modules reside in a modules folder.

Modules can be instanciated multiple times but, you can't use roles inside the module itself.

.. code-block:: bash
    test.npf:

    %variables
    MAX_CLOCK=30

    %import@client clock
    %import@server clock

    modules/clock.npf:
    %script
    for i in seq($MAX_CLOCK) ;
    do
        echo "$(hostname)-$i-RESULT-CLOCK $i"
        sleep 1
    done

pyexit
------

NPF will extract all results prefixed by *RESULT[-VARNAME]*. If VARNAME
is in result\_add={...} config list, occurences of the same VARNAME will
be added together, if it is in the result\_append config\_list, results
will be append as a list, else the VARNAME will overwrite each others.

To do more, one can use the %pyexit section to interpret the results :

.. code-block:: python

    %pyexit
    import numpy as np
    loss=RESULTS["RX"] - RESULTS["TX"]
    RESULTS["LOSS"]=loss

Any python code will be accepted, so one may compute variance among
multiple results, etc. Name space results are available under KIND\_RESULTS.

Constants
=========

Multiple constants can be used in the files and scripts sections: 
    - NPF\_ROOT : Path to NPF
    - NPF\_BUILD\_PATH: Path to the build folder of NPF 
    - NPF\_REPO: Path to the repository under test
    - NPF\_TESTSCRIPT\_PATH: Path to the location of the test script path
    - NPF\_RESULT\_PATH: Path to the result folder (by default when the command is run, or as passed by the --result-path option)
    - NPF\_OUTPUT\_PATH: Path to the output folder (by default as result,unless given with --output-filename)
    - NPF\_NODE\_ID: Index of the node used for the same role, in general 1
    - NPF\_NODE\_MAX: Number of nodesrunning the same role, in general 1
    - NPF\_MULTI\_ID: Index of the script when running multiple times the same script on each node usingthe "multi" feature, in general 1
    - NPF\_MULTI\_MAX: Number of multi as given to the cluster config (default is 1)

Test scripts shipped with NPF
=============================

Generic
-------

Generic tests are used to do black-box testing, they are L2/L3
generators, packets trace replay and HTTP generators.

They are generic in the sense that you could use them out of the box to
test any device under test in the middle of a client and a server.

-   generic\_dpdk : DPDK-based tests, need a DPDK environment setted up
-   generic : Other tests using the normal OS stack

