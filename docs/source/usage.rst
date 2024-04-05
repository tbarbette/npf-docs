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

NPF uses a **cache** of the results it obtains. 
When the same experiment for the same variables and version of the repository is run again, the test is not excuted but rather the values from the cache are used instead.
To ignore the cache, use ``--force-retest``.

Limitations
===========

There are known limitations for which solutions will be brought to NPF.

Local build only
----------------
Software described in ``.repo`` files are built locally.
When NFS or sshfs is not used, NPF copies binaries locally built to each computer of the cluster when running the test. 
Issue `#5 <https://github.com/tbarbette/npf/issues/5>`_ tracks this limitation.
