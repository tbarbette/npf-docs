
=========
Variables
=========
In the `variables` section, or through the `--variables`, one can list variables that will be replaced in any script or file section (searching for pattern $VARIABLE or ${VARIABLE}).

A variable can describe its values to take using multiple schemes:
 - LENGTH=60 Single value
 - LENGTH=[60+1024] All values between 60 and 1024, included
 - LENGTH=\[64\*1024\] All values starting from 64 multiplied per 2 up to 1024
 - LENGTH={60,64,128,256,1024,1496} A list of values
 - LENGTH=EXPAND(Hello $VARIABLE) will generate one string "Hello ..." for each value of the previously defined variable. For instance if VARIABLE=[1-10] then LENGTH will be equal to {Hello 1,Hello 2, ..., Hello 10}
 - LENGTH=RANDOM(A,B) Generate a pseudo-random number between A and B, that can be previously defined variables. It's pseudo-random so for the same run the value will be the same, and when re-executing the test the value will be the same accross execution
 - LENGTH=HEAD(A,$VARIABLE[,JOIN]) Takes the first A (A can be a previously define variable itself) values of $VARIABLES and joins them
 - LENGTH=IF(COND,A,B) Evaluates COND, and return A if COND is true or B if it isn't 

```
%variables
NUMBER=[1-10]

%script
ADD=$(echo "$NUMBER + $NUMBER" | bc)
MULT=$(echo "$NUMBER * $NUMBER" | bc)
echo "RESULT-ADDITION $ADD"
echo "RESULT-MULT $MULT"
```
The example above will re-execute the test (script) for all "NUMBER" from 1 to 10. The following graphs will be automatically produced:
![sample picture](examples/tests-readme-ADDITION.png "Result for ADDITION")
![sample picture](examples/tests-readme-MULT.png "Result for MULT").

See [the main README](../README.md#graphing-options) to style the graph and change units, axis names, etc...


Variables can optionaly be prefixed with a tag and a colon to be included only
if a tag is given (by the repo, or the command line argument):
 - cpu:CPU={0,1} If the tag cpu is given, $CPU will be expanded by 0 and 1
 - -cpu:CPU=1    If the tag cpu is not given, $CPU will be expanded by 1

This allows to do more extanded tests to grid-search some value, but do not include that in regression test


Experimental design
===================

Allow to define covariables and then use experimental design matrix to
propose values in a range

Take the following example:
.. code-block::
    A=[1-10]
    B=[1-10]

This would lead to 100 tests, for (A=1, B=1), (A=1, B=2) ... (A=10,
B=10)

Now a covariable such as this will make variables move together:

.. code-block::
    {
        A=[1-10]
        B=[1-10]
    }

Will lead to 10 tests, (A=1,B=1), (A=2, B=2) ... (A=10, B=10)

The new parameter for ranges allows to draw values from a matrix of
equal distances (see J. Santiago, M. Claeys-Bruno, and M. Sergent. Construction of Space-Filling Designs using WSP Algorithm for High Dimensional Spaces. Chemometrics and Intelligent Laboratory Systems, 113, 2012.), such as this:

.. code-block::
    {
        A=[1-1000#]
        B=[1-10000#]
        C=[1-2000000#]
    }
    
Definitely, no one wants to execute 2M*10K*1K=10^13 runs. A range with
no step (nothing after the #) will take 95 values out of the range, in a
way that the distance between all points in A, B and C is optimal (as
defined in WSP). Also, the value accross multiple runs will always be
the same, so the experiments are reproducibles.

Now that will still have 4 variables with different values, and the
plot would probably not look like what you'd want. So the configuration
option var_aggregate now accepts lists:

.. code-block::
    %config
    var_aggregate={A+B+C:all}

All points will be combined as a single run and will just be considered
as "variance" of the other variables.

In the following exemple, a "X={0,1}" variable is defined, and many other variables that are aggregated using *var_aggregated* as defined above. This is generated from the script `integration/exeperimental.npf <https://github.com/tbarbette/npf/blob/master/integration/experimental.npf>`__

.. image:: https://github.com/tbarbette/npf/raw/master/integration/experimental.png
  :width: 400
  :alt: Exemple of aggregated results in an other variable
  
.. note::

 TODO: Display this graph as a CDF
