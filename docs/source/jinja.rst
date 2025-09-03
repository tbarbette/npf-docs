.. _jinja:

*************************
Meta-scripting with jinja
*************************

Script and files can use the Jinja templating. To enable jinja in those sections, add the ``jinja`` keyword before other parameters, as shown in the example below.

Jinja
-----
Jinja variable replacement use double brackets, e.g. ``{{ VAR }}``. All NPF variables are passed to jinja, as well as the supplementary environnement variable given in `:ref:variables`.

The most useful jinja primitive is definitively the for loop :

.. code-block:: jinja

    {% for i in range(N) %}
        Do something with {{i}}
    {% endfor %}

While bash scripts can implement for loop by themselves, this is especially useful to generate configuration files, or keep scripts clean.

Another useful situation is to change a part of a configuration file according to the given parameters. For instance for an nginx web server:

.. code-block:: jinja

    {% if HTTP2 %}
     	    listen 443 http2 reuseport;
    {% else %}
            listen 80 reuseport;
    {% endif %}

The complete jinja documentation can be found at https://jinja.palletsprojects.com/en/3.1.x/.

Example
-------

Below is an example of the script using the jinja templating.

.. code-block:: bash

    %config 
    results_add={SUM}

    %variables
    TERMINAL=[1-8]

    %script@client jinja delay=1
    {% for P in range(TERMINAL) %}
        echo "RESULT-SUM {{P}}"
    {% endfor %}

This script will run multiples times (for TERMINAL=8, 8 times) the echo line.
In this case it means the metric "SUM" will appear multiple times.
The ``result_add`` config tells NPF to do the sum of all values.

Deprecated python inline python
-------------------------------
Jinja is the way to go.
But you might come accross replacement like ``$(( ... ))``, which is a trick to invoke a python context.
This was often used to generate lists, but it's limited to inline and is rather complicated.

For instance, to generate a configuration list with some increasing integer :

.. code-block:: jinja

    $(( ", ".join([ "%d" % i for i in range(N) ]) ))

The jinja equivalent is actually simpler and safer:

.. code-block:: jinja
    
    {{ range(N)|join(', ') }}
