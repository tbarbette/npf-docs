.. _enoslib_integration:

Enoslib Integration (Grid5000 / CloudLab / Chameleon)
=====================================================

NPF provides built-in integration with `Enoslib <https://discovery.gitlabpages.inria.fr/enoslib/>`_, a library designed to facilitate the execution of reproducible experiments on large testbeds such as Grid'5000, Chameleon Cloud, and CloudLab, as well as local environments using Vagrant.

This integration allows NPF to seamlessly allocate resources, configure networking, deploy dependencies, and run tests on these infrastructures without modifying your core ``.npf`` test scripts.

Using Enoslib with NPF
----------------------

Instead of using a static cluster file (``.node``) to define machines, you can define an Enoslib script to dynamically provision resources and pass them to NPF. 

Typically, you use an Enoslib Python script or a Jupyter Notebook to:

1. **Allocate resources**: Define the provider (e.g., Grid5000), the number of machines, clusters, and networks.
2. **Retrieve the roles**: Once resources are provisioned, Enoslib maps these machines to specific roles (like ``client`` and ``server``).
3. **Execute commands or tests**: You can execute commands across these roles.

Example with Localhost
----------------------

You can start by testing Enoslib locally to familiarize yourself with the API:

.. code-block:: python

   import enoslib as en

   # Initialize logging
   en.init_logging()

   # Define roles targeting localhost
   roles = {
       "client": en.Host("localhost", user="yourusername"),
       "server": en.Host("localhost", user="yourusername")
   }

   # Run a basic command across all roles
   en.run_command("date", roles=roles["client"])

Grid'5000 Example
-----------------

To use Grid'5000, you will define the `G5k` provider and specify the desired cluster requirements:

.. code-block:: python

   import enoslib as en

   en.init_logging()

   # Configure Grid5000 network and compute requirements
   network = en.G5kNetworkConf(type="prod", roles=["my_network"], site="rennes")
   
   conf = (
       en.G5kConf.from_settings(job_name="npf_experiment", walltime="02:00:00")
       .add_network_conf(network)
       .add_machine(roles=["client"], cluster="paravance", nodes=1)
       .add_machine(roles=["server"], cluster="paravance", nodes=1)
   )

   provider = en.G5k(conf)
   
   # Allocate resources and get roles
   roles, networks = provider.init()

   # Once resources are ready, NPF can leverage these roles
   # You can execute shell commands, deploy NPF, or orchestrate complex scenarios
   en.run_command("echo 'Ready for NPF!'", roles=roles)

   # Clean up after experiment
   provider.destroy()

For more advanced configurations and examples, refer to the `Enoslib Documentation <https://discovery.gitlabpages.inria.fr/enoslib/>`_.
