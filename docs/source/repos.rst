.. _repos:

************
Repositories
************

All repositories are defined in the repo folder. A repo configuration define how
to fetch and install a specific program, using one of the following ways :  
                  
*  **git** : Use git to download and compile a branch or specific commit
*  **get** : Download a file and compile/install it if needed           
*  **package** : Use the OS package manager (only Red-Hat and Debian based supported for now) (TODO : Still not implemented)   
  
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

Tags can be used to activate some optional lines as in *variables* sections.


Repo can inherit others. For instance, the following file inherits *click* and add an option to the configure line to enable IPv6:

.. code-block:: bash

    name=Click with IPv6
    parent=click
    url=https://github.com/kohler/click.git
    configure=./configure --disable-linuxmodule --enable-userlevel --enable-user-multithread --enable-etherswitch --enable-bound-port-transfer --disable-dynamic-linking --enable-local --enable-ip6