.. _regress:

Regression Testing
==================

NPF includes powerful tools for tracking performance regressions across software versions or git commits. This helps you identify if a specific commit degrades the performance of your system.

Two main tools are provided to handle regressions: ``npf-regress`` and ``npf-watch``.

npf-regress
-----------

The ``npf-regress`` tool is used to evaluate the performance of a software repository across multiple commits or versions and generate graphs comparing them. 

You can use it similarly to the standard ``npf`` command, but with additional options for tracking history.

.. code-block:: bash

   npf-regress <repository_name> --test <test_script.npf> --history <N>

**Key Options:**

* ``--history N``: Determines how many commits in the history to execute the regression tests on. By default, it is 1, meaning it compares the current ``HEAD`` against ``HEAD~1``. Setting this to ``N`` evaluates the last ``N`` commits.
* ``--compare-version <version>``: Specifies a specific previous version to compare against the latest version. By default, it takes the first parent of the last version that has results.
* ``--regress-version <version1> <version2> ...``: Compare explicitly against multiple specific old versions.
* ``--branch <branch>``: Compare against a specific branch.
* ``--allow-old-build``: Allows NPF to rebuild and run tests for old versions if the results are not cached.

**Comparing Specific Versions:**

To compare your current local build against a specific tag, such as ``v1.0``:

.. code-block:: bash

   npf-regress my_repo --test my_test.npf --compare-version v1.0

npf-watch
---------

If you want to integrate NPF into a continuous testing suite or actively monitor a repository you don't own to ensure performance remains stable, use ``npf-watch``.

This tool runs in a loop, watching for new commits in a given list of repositories. When a commit is made, it runs the specified tests and can send an email with the results and generated graphs if a regression occurs.

.. code-block:: bash

   npf-watch <repository_name> --test <test_script.npf> --interval 3600 --mail-to devteam@example.com

**Key Options:**

* ``--interval <secs>``: The interval in seconds between repository polls (default is 60).
* ``--mail-to <email>``: A list of email addresses to send the report to.
* ``--mail-from <email>``: The sender email address.
* ``--mail-erroronly``: If set, an email will only be sent when a test fails or performance regressions are detected (the default behavior).
* ``--onerun``: Perform only one loop of regression testing instead of running continuously. Useful for CI/CD pipelines.

When an email is sent, it includes an HTML body detailing the passed and failed constraints alongside inline images of the performance graphs.
