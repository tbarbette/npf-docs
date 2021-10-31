=====
Usage
=====

.. _installation:

Install
=======

To use NPF, first install it using pip:

.. code-block:: console

   (.venv) $ pip install npf

On ubuntu, you can simply do:

.. code-block:: console

    $ sudo apt install python3-pip && python3 -m pip install --user npf
    
Run-time dependencies
=====================

SSH
---
Cluster-based tests use SSH to launch multiple software on different nodes, therefore SSH should be setup on each node for a password-less connection. Use public key authentication and be sure to add the ssh keys in your ssh agent using `ssh-add` before running NPF.

sudo (optional)
---------------
Most DPDK-based but also other scripts use the `sudo=true` parameter in test scripts to gain root access. You can either always connect as root to other servers (see the :ref:`cluster` section) or set up password-less sudo on all nodes.

File-sharing (optional)
-----------------------
Use either a NFS shared mounted on all nodes or sshfs to mount the local NPF folder on all nodes. The path to the shared NPF root can be different on each node, see the cluster section below.
If this is not the case, the dependencies (software built by NPF) will be sent to all nodes that will use them in the corresponding scripts through SSH, but it is slower.


The big picture
===============

.. code-block::

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

Your *.npf* test file is composed of a serie of sections, as in the example given above. The sections describe the scripts to run, where to run them, what variables should be tested, what are their ranges, configuration parameters such as timeout or graph colors, etc. Each section is described in more details in :ref:`tests`. 
When launching NPF, you will also give the name of one or more *repositories*, which are files located in the `repo` folder describing software to download, install and compile so everything is in place when your experiment is launched. They follow a format descrived in :ref:`repos`.
Your test script will also define a few script *roles*, such as `client` or `server` as in the example above. When you actually launch your experiment, you must tell which machine (physical or virtual) will take the role. For simple cases, passing the address of a machine with the `--cluster role=machine` will be enough. When you'd like to define parameters such as IPs and MAC addresses, you can define a *cluster* file that will describe details about each machines. See :ref:`cluster` for more details.


