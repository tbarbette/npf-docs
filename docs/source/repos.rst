.. _repos:

************
Repositories
************

All repositories are defined in the repo folder. A repo configuration define how
to fetch and install a specific program, using one of the following ways :  
                  
*  **git** : Use git to download and compile a branch or specific commit
*  **get** : Download a file and compile/install it if needed           
*  **package** : The repository is a package of the system, installed with its package manager (Debian-based and Red Hat-based systems). See `System packages`_.
  
The *git* method supports the "history" parameter, allowing to go back in commit history to rebuild the history with older versions (commits). *get* and *package* have a hardcoded version in the repo file.
The default method is *git*.          

This is the example file to download and build click:

.. code-block:: bash

    name=Click
    branch=master
    url=https://github.com/kohler/click.git
    method=git
    bin_folder=bin
    bin_name=click
    configure=./configure --disable-linuxmodule --enable-userlevel --enable-user-multithread --enable-etherswitch --enable-bound-port-transfer --disable-dynamic-linking --enable-local
    clean=make clean
    make=make
    intel:configure+=--enable-intel-cpu
    tags=click,vanilla

* The `branch` parameter allows to select a specific branch.
* The `url` parameter is the path to the *git* repository, or the tarball when using *get*.
* `bin_folder` allow to export automatically a PATH environment variable, so one can simply use the executable without referencing the path in their *script* sections.
* `bin_name` is an optional binary name to verify the build was successful. It should be found in `bin_folder`.
* `configure` is a first step of build, by default it is "./configure" if omitted, but can be left empty to pass the configure phase.
* `clean` is launched after configure to ensure a clean build when a new version is downloaded. By default it is "make clean" if omitted, but can be left empty to pass the cleaning phase.
* `make` is the command to launch the build process *per se*. By default it is "make" if omitted, but can be left empty to pass the bulding phase.
* `tags` will automatically enable some tags when using this repository.
* `version` (only for the get method) allows to define a version to tager. $VERSION can be used in the `url`.
* `packages` lists the system packages the repository needs, see `System packages`_.

Tags can be used to activate some optional lines as in *variables* sections.

System packages
===============

A repository can list the system packages it needs to build, separated by commas or spaces.
A name that differs between Debian-based and Red Hat-based systems is prefixed with ``deb:`` or ``rpm:``.
For instance, snort needs libdumbnet:

.. code-block:: bash

    name=Snort
    method=get
    packages=deb:libdumbnet-dev,rpm:libdnet-devel

Before building the repository, NPF checks the packages with ``dpkg-query`` or ``rpm`` on the node that builds it: locally, or on each node with ``--remote-build``.
When some are missing, NPF prints the command that installs them.
With ``--install-packages``, it installs them itself, with ``sudo`` and ``apt-get`` or ``dnf``.
As a library installed from source is missing for the package manager, a missing package is only a warning, and NPF still tries to build.

With ``method=package``, the repository is the package itself, and a missing package stops the test.
``packages`` defaults to the name of the repository, and ``bin_folder`` to ``/usr/bin``. For instance, to use the iperf3 of the system, write a ``repo/iperf3.repo`` with:

.. code-block:: bash

    name=iperf3
    method=package
    bin_name=iperf3

The version of such a repository is the ``version`` given in the repo file, if any.


Repo can inherit others. For instance, the following file inherits *click* and add an option to the configure line to enable IPv6:

.. code-block:: bash

    name=Click with IPv6
    parent=click
    url=https://github.com/kohler/click.git
    configure=./configure --disable-linuxmodule --enable-userlevel --enable-user-multithread --enable-etherswitch --enable-bound-port-transfer --disable-dynamic-linking --enable-local --enable-ip6
Command-Line Repository Syntax
------------------------------

When specifying a repository on the command line (e.g. as an argument to `npf-run` or `npf-regress`), you can use the following syntax to override the version, target a specific role, or change the display title:

``repo[%version][@role][:Title]``

* ``%version`` allows you to override the branch, tag, or commit to build (e.g. ``click%master``).
* ``@role`` forces NPF to only build and deploy the repository on the nodes assigned to a specific role (e.g. ``iperf2@server``). This skips sending and building the package on other machines.
* ``:Title`` overrides the human-readable title of the repository for graphs and output logs (e.g. ``iperf2:My Custom IPerf``).

You can combine these as well: ``iperf2%2.0.9@client:Old Iperf``
