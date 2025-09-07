.. _variables:

=========
Variables
=========

In the ``%variables`` section and through the ``--variables`` argument, one can list variables for a test script.
NPF generates executions of a test scripts to explore the combinations of values that variables defined in the script can take.
Values of a variable named ``LENGTH`` can be retrieved with patterns ``$LENGTH`` or ``${LENGTH}`` in ``%script`` and ``%file`` sections of a test file.

A variable can describe its values using multiple schemes:

``LENGTH=60``
    Single value
``LENGTH=[60-1024]`` 
    All values between 60 and 1024, included
``LENGTH=[100-1000#100]``  
    All values between 100 and 1000 by step of 100.
``LENGTH=[64*1024]``
    All values starting from 64 multiplied per 2 up to 1024
``LENGTH=[64*1024#4]``
    All values starting from 64 multiplied per 4 up to 1024
``LENGTH={60,64,128,256,1024,1496}``
    A list of values

Advanced
--------

The following are advanced variables, if you're beginning in NPF, stick with the ones above.

``LENGTH=RANDOM(A,B)``
    A pseudo-random number between A and B, which can be previously defined variables. 
    A value is generated for each execution and kept for all runs of a given execution.
``LENGTH=EXPAND(Hello $VARIABLE)``
    A list of string starting with "Hello" for each value of the previously defined ``$VARIABLE``. When ``VARIABLE=[1-10]`` then ``LENGTH`` is ``{Hello 1,Hello 2, ..., Hello 10}``.

.. note::

    By default, an experiment will try every combination of variables, which is often called "grid-search" or "full factorial design". Check the :ref:`experimental design<expdesign>` page to learn how to explore a large parameter space.


Tags
====

Variables can be omitted or included based on a tag, given by a ``repo`` or the ``--tags tag [tag ...]`` argument.
These variables are prefixed in the ``%variables`` section with a tag and a colon.

For instance:

``cpu:CPU={0,1}``
    When the ``cpu`` tag is given, ``$CPU`` take values 0 and 1. Otherwise, ``$CPU`` is omitted.

``cpu:CPU=1``
    When the ``cpu`` tag is given, ``$CPU`` takes the value 1. Otherwise, ``$CPU`` is omitted.

This allows to do more expanded tests to grid-search some value, but do not include that in regression test.

Example
=======

The following test script defines a single variable and computes two results.

.. code-block::text

    %variables
    NUMBER=[1-10]

    %script
    ADD=$(echo "$NUMBER + $NUMBER" | bc)
    MULT=$(echo "$NUMBER * $NUMBER" | bc)
    echo "RESULT-ADDITION $ADD"
    echo "RESULT-MULT $MULT"

NPF executes the above test script by running the script sections for all values of ``$NUMBER``, i.e. from 1 to 10. 
NPF also produces the two following graphs in result:

.. image:: https://github.com/tbarbette/npf/raw/main/examples/doc-variable-example-ADDITION.png
    :alt: "Graph for RESULT-ADDITION"

.. image:: https://github.com/tbarbette/npf/raw/main/examples/doc-variable-example-MULT.png
    :alt: "Graph for RESULT-MULT"

See the :ref:`graphing page<graph>` to style the graph and change units, axis names, etc...

See the :ref:`experimental design<expdesign>` page to learn how to explore a large parameter space.


.. _aggregate:

Covariables
===========

NPF allows to define covariables that move together.

.. code-block:: bash

    A=[1-10]
    B=[1-10]

In the above example, NPF would run 100 tests, for (A=1, B=1), (A=1, B=2) ... (A=10,
B=10).

A covariable makes variables move together:

.. code-block:: bash

    {
        A=[1-10]
        B=[1-10]
    }

The above example leads to 10 tests, (A=1,B=1), (A=2, B=2) ... (A=10, B=10).

This is also useful to pair variables, for instance if a configuration depends on another. Say for instance you want a specific number of cores for a given throughput:

.. code-block:: bash

    {
        RATE={10,50,100}
        CORES={2,4,5}
    }

This will run 3 tests, (RATE=10, CORES=2), (RATE=50, CORES=4), (RATE=100, CORES=5)

Our example still defines 2 variables, and the resulting
plot may not be appropriate by representing the evolution of these variables separately. 
In this case, the ``var_aggregate`` configuration option can be used with a list:

.. code-block:: bash

    %config
    var_aggregate={A+B:all}

    %variables
    A=[1-10]
    B=[1-10]
    X={0,1}

In this example, all points are combined and considered
as additional runs of the other variables.

The following graph is the result of executing the test script example with an additional ``X={0,1}`` variable is defined.
``A``, ``B`` variables are aggregated using ``var_aggregated`` as explained above.

.. image:: https://github.com/tbarbette/npf/raw/main/integration/experimental.png
  :width: 400
  :alt: Exemple of aggregated results in an other variable
  
.. note::

    The :ref:`graphing page<graph>` gives more details on ways to tweak graphs and choose a better representation.
