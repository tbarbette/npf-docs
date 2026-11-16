.. _usage:

*****
Usage
*****

.. _installation:

Install
=======

NPF can be installed using pip in a Python 3 environment:

.. code-block:: console

   (.venv) $ python -m pip install npf

On Ubuntu, a local install can be achieved with:

.. code-block:: console

    $ sudo apt install python3-pip && python3 -m pip install --user npf
    
Run-time dependencies
=====================

SSH
---
NPF use SSH to run tests on a computer cluster. Therefore SSH should be setup on each node for a password-less connection.
Use public key authentication and add the required ssh keys to your ssh agent using ``ssh-add`` before running NPF.

sudo (optional)
---------------
Most DPDK-based scripts and scripts using the ``sudo=true`` parameter in scripts roles to use root priviledge. 
You can either connect as root to the cluster (see the :ref:`cluster` section) or set up password-less sudo on all nodes.

File-sharing (optional)
-----------------------
In general, NPF is used to run one or more scripts and programs over multiple machines.
By default, NPF assumes the current folder is synchronized on all machines. For instance, using NFS or sshfs.
NPF can also copy files by itself over NFS is there is no file sharing in place.
The :ref:`cluster` section details way to define the use of file sharing and synchronize different paths.


The big picture
===============

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

A *.npf* test script is composed of a series of sections, as illustrated in the above example.
The sections describe the variables to test and their ranges, the code that must be run for each computer in the cluster, but also configuration parameters such as timeout, graph colors, etc...
Each section is described in more details in :ref:`tests`. 

A test script also defines several script *roles*, such as ``client`` or ``server`` as in the above example.
Each bash code snippet will be executed by its corresponding role. 
In our example, the ``server`` role starts an iPerf3 server in the background 
while the ``client`` role starts an iPerf3 client with several arguments with values taken from variables defined in the test script.
In this example, ``PARALLEL`` takes values from 1 to 8, while ``ZEROCOPY`` takes either ``-Z`` or an empty string as value.
More complex meta-scripting can be done using :ref:`jinja`.

When running the script, roles are associated to computers in the cluster in two manner. 
First, through the command line by passing pairs of role and address with ``--cluster role1=address1 role2=address2``.
Second, by defining a *cluster* file describing details about each computer of the cluster.
A cluster file can contain advanced parameters such as interface names, IPs and MAC addresses. 
See :ref:`cluster` for more details.

When launching NPF, one or more *repositories* can be optionnally specified.
These are files located in the ``repo`` folder that describe software to download, compile and install. 
Their format is described in :ref:`repos`.
Using repositories ease the reproducibility of your experiment.
These are optional and NPF uses a repository named "local" by default, which do not compile nor install software.

.. note::
   It is advised to start using NPF without repositories or dependencies handled by NPF.
   When some familiarity with NPF is gained, start using its dependencies chains and build process.

NPF maintains a **cache** of the results it obtains. 
When the same experiment for the same variables and version of the repository is run again, by passing the ``--cache`` argument, the test will not be executed. 
Instead, the values from the cache will be used.
This is convenient when you try many variables and then restrict some of them to get a simpler graph, without re-executing the actual test.
Note that if some results are missing (for example, if you added more metrics since the last run, or if there are less points in the cache than the number of runs requested), NPF will still launch the test to complete the missing points.

Keeping track of what a test did
================================

``--debug``
    prints when each script starts, is stopped and ends, and with which exit code.

``--preserve-temporaries``
    keeps the folder in which NPF ran the test, with the files of the test.
    It also holds the output of each script in ``<name>.stdout`` and ``<name>.stderr``, e.g. ``dut_0.stdout`` for the first script of the ``dut`` role.
    The output of each run follows a line that tells the variables of the run and its repetition, the node, how the script ended (its exit code, stopped by NPF at the end of the run, timeout...) and how long it ran.
    With ``--preserve-temporaries=folder``, the test folder is moved to ``folder``, which can contain variables.

The graphs
    The PDF file of each graph holds what is needed to draw it again: the command line and the folder it ran from, the versions of NPF and of the series, the test scripts, and the results as CSV. ``pdfinfo -custom graph.pdf`` shows them.

Building on the nodes
=====================

By default, software described in ``.repo`` files is built locally.
When the folder of the experiment is not shared with a node (``nfs=0`` in its cluster file), NPF copies the build folder to it.
With ``--remote-build``, each node builds the software itself, against its own libraries: a node file can give these builds variables with ``env=`` lines, e.g. ``env=PKG_CONFIG_PATH=...`` for the DPDK of that node (see :ref:`cluster`).

.. _cmdline:

Command-line options
====================

``npf``, ``npf-regress`` and ``npf-watch`` share the options below. ``--help`` prints them with the options of each tool.

``npf`` takes the repositories to compare, as ``repo[+VAR=VALUE][:Title]`` (see :ref:`repos`), and ``--graph-title`` *TITLE* to set the title of the graphs.
``npf-regress`` and ``npf-watch`` have their own options, described in :ref:`regress`:

* ``npf-regress``: ``--allow-old-build``, ``--force-old-build``, ``--regress``, ``--history`` *N*, ``--branch`` *BRANCH*, ``--compare-version`` *VERSION*, ``--regress-version`` (or ``--graph-version``) *VERSION...*, ``--regress-history`` (or ``--graph-num``) *N*.
* ``npf-watch``: ``--interval`` *SECONDS*, ``--history`` *N*, ``--graph-num`` *N*, ``--mail-to`` *EMAIL...*, ``--mail-from`` *EMAIL*, ``--mail-erroronly``, ``--mail-smtp`` *ADDRESS*, ``--onerun``.

Verbosity options
-----------------

``--show-full``, ``--show-all``
    Deprecated : show full execution results, this is now the default. Use --quiet instead.

``--show-files``
    Show content of created files.

``--show-cmd``
    Show the executed script.

``--show-time-results``
    Show time results.

``--no-colors``
    Do not use terminal colors.

``--quiet``
    Quiet mode.

``--quiet-regression``
    Do not tell about the regression process.

``--debug``
    Debug mode : show scripts execution and termination and more information about synchronization. With --preserve-temporaries, also tells in which file the output of each script is kept.

``--quiet-build``
    Do not tell about the build process.

``--show-build-cmd``
    Show build commands.

``--version``
    Print the version of NPF and exit.

Building options
----------------

``--use-local`` *USE_LOCAL*
    Use a local version of the program instead of the automatically builded one.

``--install-packages``
    Install the system packages that the repositories need (packages= in their .repo file) when they are missing, with sudo and apt-get or dnf. Without it, NPF tells how to install them.

``--no-build``
    Do not build the last version, use the currently compiled one.

``--force-build``
    Force to rebuild even if the current version is matching the regression versions (see --regress-version or --history).

``--no-build-deps`` *NO_BUILD_DEPS*
    Do not build the last version of some dependencies, use the currently compiled one.

``--ignore-deps`` *IGNORE_DEPS*
    Do not use the specified dependencies, find binaries in the current path instead.

``--force-build-deps`` *FORCE_BUILD_DEPS*
    Force to rebuild some dependencies.

``--remote-build``
    Build dependencies and repos on the remote machines instead of locally.

Testing options
---------------

``--no-test``
    Do not run any tests, use previous results.

``--no-supplementary-test``
    Do not run supplementary tests for regression, use previous results.

``--force-test``
    Force re-doing all tests even if data for the given version and variables is already known, but append the new data to exesting one.

``--force-retest``
    DEPRECATED. Now the default is to ignore the cache. Use --cache instead.

``--cache``
    Use data from the previous experiments. If the same combination of variables was already tried, do not re-run the experiment but keep results. This allows fast exploration of the parameter space.

``--no-init``
    Do not run any init scripts.

``--no-conntest``
    Do not run connection tests.

``--max-results``
    Count the number of valid previous tests as the maxium number of points in all tests, instead of the minimum.

``--preserve-temporaries`` *PRESERVE_TEMP*
    Do not delete test folder with temporary files. The output of each script is kept there, in <script name>.stdout and .stderr, each run after a line telling its variables, its node and how the script ended. If a value is provided, each test result will be moved to that folder. The folder path may contain variable values to do the replacement.

``--use-last`` *USE_LAST*
    Use data from previous version instead of running test if possible.

``--result-path``, ``--result-folder`` *path*
    Path to NPF's own database of results. By default it is a "result" folder.

``--tags`` *tag*
    list of tags.

``--variables`` *variable=value*
    list of variables values to override.

``--config`` *config=value*
    list of config values to override.

``--env`` *list of variables*
    list of environment variables to pass in scripts.

``--test``, ``--npf`` *path or test*
    script or script folder. Default is tests.

``--python-inline``
    Evaluate $(( )) in all scripts and files as Python expressions, as before. Prefer adding python-inline to the sections that need it, or jinja templates.

``--build-folder``, ``--build-path`` *path*
    Set where dependencies would be built. Defaults to npf's folder itself, so dependencies are shared between test scripts.

``--experiment-folder``, ``--experiment-path`` *path*
    Where to create temporary files and execute tests from. Default to local directory. Tests will always be executed from a temporary-made folder inside that path. Beware if you do not have a similar NFS/SSHFS based directory identical on all nodes, the "path" argument of the cluster file must match this repository, same as the build path relative to that directory.

``--search-path`` *path*
    Search for various files in this directories too (such as the parent of your own repo, cluster or modules folder).

``--no-mp``
    Run tests in the same thread. If there is multiple script, they will run one after the other, hence breaking most of the tests.

``--exp-design`` *DESIGN*
    Experimental design method.

``--spacefill`` *SPACEFILL*
    The path towards the space filling values matrix.

``--rand-env`` *RAND_ENV*
    Add an environmental variable of a random size to prevent bias.

Cluster options
---------------

``--cluster`` *role=user@address:path [...]*
    role to node mapping for remote execution of tests. The format is role=address[,option=value,...] . Address can be an address or a file in cluster/address.node describing supplementary parameters for the node.

``--cluster-autosave``
    Automatically save NICs found on the machine. If the file cluster/address.node does not exists, NPF will attempt to auto-discover NICs. If this option is set, it will auto-create the file.

``--no-ssh-config``
    Do not use the SSH config file (~/.ssh/config) when connecting to remote nodes.

Output data
-----------

``--web`` *WEB*
    Generate interactive graphs in a \*.html file format.

``--notebook``, ``--nb`` *NOTEBOOK_PATH*
    Generate a Jupyter Notebook that plots the data (\*.ipynb file format).

``--template-nb`` *TEMPLATE_NB_PATH*
    Use a custom Jupyter Notebook as template. Default: the one of NPF.

``--nb-kernel`` *NB_KERNEL*
    Specify which kernel to use for executing the Jupyter Notebook.

``--update-nb``
    If the notebook already exists, try to update the experiment data (cell containing "data = ").

``--force-nb``
    If the notebook already exists, overwrite it (the previous data and code will be lost).

``--disable-nb-exec``
    By default the output notebook is executed, this option disables that feature.

``--output`` *OUTPUT*
    Output data to CSV files, one per result type. By default it prints the variable value as first column and the second column is the mean of all runs. Check --output-columns to change this behavior.

``--output-columns`` *OUTPUT_COLUMNS*
    Columns to print in each --output CSV files. By default x mean. Valid values are mean/average, min, max, perc[0-9]+, med/median/perc50, std, nres/n, first, last, all. Check the documentation for details.

``--single-output``, ``--pandas``, ``--csv`` *pandas_filename*
    Output a dataframe to CSV with all result types as columns, and one line per variables and per runs. This is a pandas dataframe, and can be read with pandas easily again. Time series are each outputed in a single different CSV.

Graph options
-------------

``--graph-size`` *INCH*
    Size of graph.

``--graph-filename`` *graph_filename*
    path to the file to output the graph.

``--show-serie``
    always add the serie name in the file path.

``--graph-reject-outliers``
    Do not plot the outliers: the values further from the mean than accept_outliers_mult (see %config) standard deviations.

``--graph-no-series``
    With a single series, do not make series of the values of a dynamic variable.

``--graph-group-repo``
    Group series, using the repository name as a variable.

``--graph-group-series``
    Group series with the same name.

``--keep-parameters``
    Do not remove parameters from the dataset. By default, variables which have the same values for the entire dataset are removed before the dataset is passed to output modules (CSV, graphs, web, ...). This option keeps them.

``--no-transform``
    Forbid automatic transformation of data such as extracting a variable as a serie.

``--graph-select-max`` *GRAPH_SELECT_MAX*
    Only keep the first X results for each run.

``--graph-dpi`` *GRAPH_DPI*
    Resolution of the graphs, in dots per inch. Default: 300.

``--no-graph-time``
    Do not plot time series graphs.

``--no-graph``
    Do not plot graphs.

``--graph-keep-variables`` *GRAPH_KEEP_VARIABLES*
    Keep specific variables dynamic when there are more dynamic variables than graph_max_variables.

``--iterative``
    Graph after each results, allowing to get a faster glimpse at the results.

``--onefirst``
    Do a first pass with one run per variables, then do the last runs.

Statistics options
------------------

``--statistics`` *STATISTICS*
    Give some statistics output. Accepts a list of outputs names to give statistics about, or will try to find the best outputs if no value is provided.

``--statistics-maxdepth`` *STATISTICS_MAXDEPTH*
    Max depth of learning tree.

``--statistics-maxmetrics`` *STATISTICS_MAXMETRICS*
    Maximum number of metrics to give, ignored if statistics has some arguments.

``--statistics-filename`` *STATISTICS_FILENAME*
    Output of learning tree.
