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

While bash scripts can implement for loop by themselves, this is especially utile to generate configuration files, or keep scripts clean.

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
    results_add={THROUGHPUT}

    %variables
    PARALLEL=[1-8]

    %script@client jinja delay=1
    {% for P in range(PARALLEL) %}
        echo "Running client {{P}}"
        result=$(iperf3 -f k -t 2 -P 1 $ZEROCOPY -c ${server:0:ip} | tail -n 3 | grep -ioE "[0-9.]+ [kmg]bits")
        echo "RESULT-THROUGHPUT $result"
    {% endfor %}

This script will run multiples times (for PARALLEL=8, 8 times) the iperf3 client command. 
In this case it means the result "THROUGHPUT" will appear multiple times.
The ``result_add`` config tells NPF to do the sum of all.
In this situation it is needed as iperf3 is not multi-threaded, and therefore the -P parameter is rather limited to scale.

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