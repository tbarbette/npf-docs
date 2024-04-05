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
``LENGTH=[60+1024]`` 
    All values between 60 and 1024, included
``LENGTH=[64*1024]``
    All values starting from 64 multiplied per 2 up to 1024
``LENGTH={60,64,128,256,1024,1496}``
    A list of values
``LENGTH=RANDOM(A,B)``
    A pseudo-random number between A and B, which can be previously defined variables. 
    A value is generated for each execution and kept for all runs of a given execution.
``LENGTH=EXPAND(Hello $VARIABLE)``
    A list of string starting with "Hello" for each value of the previously defined ``$VARIABLE``. When ``VARIABLE=[1-10]`` then ``LENGTH`` is ``{Hello 1,Hello 2, ..., Hello 10}``.


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

.. image:: https://github.com/tbarbette/npf/raw/master/tests/examples/tests-readme-ADDITION.png
    :alt: "Graph for RESULT-ADDITION"

.. image:: https://github.com/tbarbette/npf/raw/master/tests/examples/tests-readme-MULT.png
    :alt: "Graph for RESULT-MULT"

See the :ref:`graphing page<graph>` to style the graph and change units, axis names, etc...

.. _aggregate:

Experimental design
===================

NPF allows to define covariables and then use a WSP experimental design to
sample values in a given range.

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

The ``#`` parameter defines variables with values drawn from ranges
with a minimum distance between combinations using the WSP algorithm
(see J. Santiago, M. Claeys-Bruno, and M. Sergent. Construction of Space-Filling Designs using WSP Algorithm for High Dimensional Spaces. Chemometrics and Intelligent Laboratory Systems, 113, 2012.), such as this:

.. code-block:: bash

    {
        A=[1-1000#]
        B=[1-10000#]
        C=[1-2000000#]
    }

Non-covariated variables would result ``2M*10K*1K=10^13`` runs. A range with the ``#`` parameter and no stop samples 95 combinations of values out of the defined range.
The values are sampled so that the distance between all points in A, B and C is optimal (as
defined in WSP). Also, these values are sampled deterministically, so the experiments are reproducibles.

Our example still defines 3 variables, and the resulting
plot may not be appropriate by representing the evolution of these variables. 
In this case, the ``var_aggregate`` configuration option can be used with a list:



.. code-block:: bash

    %config
    var_aggregate={A+B+C:all}

In this example, all points are combined and considered
as additional runs of the other variables.

The following graph is the result of executing the test script example with an additional ``X={0,1}`` variable is defined.
``A``, ``B`` and ``C`` variables are aggregated using ``var_aggregated`` as explained above.
This is generated from the script `integration/exeperimental.npf <https://github.com/tbarbette/npf/blob/master/integration/experimental.npf>`__

.. image:: https://github.com/tbarbette/npf/raw/master/integration/experimental.png
  :width: 400
  :alt: Exemple of aggregated results in an other variable
  
.. note::

    The :ref:`graphing page<graph>` gives more details on ways to tweak graphs and choose a better representation.