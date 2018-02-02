Contribution Guidelines
=======================

We use `Github projects`_ to organize our ticket workflow.
If you want to lend a hand, check out the current project and choose one of the tickets from the issues!
If there's `a particular issue`_ you would like to work on and it isn't already assigned, leave a comment on that issue indicating your desire to work on it.
Then, start working!

.. _Github projects: https://github.com/melinath/django-graph-api/projects/4
.. _a particular issue: https://github.com/melinath/django-graph-api/issues

Start Developing
----------------

To get started with your contribution, fork this project into your own GitHub profile and clone that forked repository to your machine.

::

    git clone https://github.com/your-username/django-graph-api.git

After cloning, navigate into the new directory.

::

    cd django-graph-api

Define a remote repository called ``upstream`` that points to the original django-graph-api repository.

::

    git remote add upstream https://github.com/melinath/django-graph-api.git

We're using `pipenv`_ as the package and environment manager for this project.
If you don't yet have it, check the link just given for instructions on how to get it on your machine.

(Note for Windows users: The ``py`` launcher cannot tell ``pipenv`` which Python version to use.
The simplest fix is to add to your path only the desired Python folder and its ``Scripts`` subfolder,
then use the commands as shown here without ``py``.)

Create a ``pipenv`` virtual environment using Python 3.6.
**Note: any code that you write should be compatible with Python 2.7, but we recommend that you develop in Python 3.6.**

::

    pipenv --python 3.6

    
Install production dependencies, and also install development-only dependencies:

::

    pipenv install
    pipenv install --dev

Verify that the existing tests pass:

::

    pipenv run pytest

(Note that if you have already activated the environment,
which you'll do in the next section,
you can run the ``pytest`` command on its own to run the tests.)

After you see that those tests pass, activate the virtual environment that ``pipenv`` set up for you and get to work!

.. _pipenv: https://github.com/pypa/pipenv


Running the Test Project
------------------------

Django Graph API comes with a sample Django project based on the Star Wars examples from `GraphQL documentation`_.
It is used for integration tests and to help with development.

If you have installed the local version of ``django-graph-api``,
then you should already have access to the source code that contains the test data.

To activate the environment:

::

    pipenv shell

Then apply the existing migrations to create a ``sqlite`` database in your repository root.

::

    python manage.py migrate

Create the test data to fill the database

::

    python manage.py create_test_data

Run the test server

::

    python manage.py runserver

You should be able to see the GraphiQL app and run queries by navigating to ``localhost:8000/graphql`` in your browser.

Continue to verify that the tests that you write for your code (as well as the existing tests) pass as you develop by running:

::

    pytest

.. _GraphQL documentation: http://graphql.org/learn/


Building the Documentation
--------------------------

Any change you make should correspond with a documentation update.
To view your changes in HTML format, you can build the documentation on your computer as follows.

If you haven't already, create an environment and install the production and development requirements.
(Do not redo this if you have already done it -- it will delete and re-create your environment.)

::

    pipenv --python 3.6
    pipenv install
    pipenv install --dev

Navigate to the ``docs`` directory, and build the docs files as html"

::


    cd docs
    make html

View the docs by opening ``_build/html/index.html`` in your browser.


Integrating Your Changes
------------------------

Once you're done writing code, you will need to open a pull request with your changes.
In order to be merged, pull requests must fulfill the following requirements:

- All new code must have tests.
- All tests must be passing.
- Any relevant documentation has been updated.

Once your pull request is complete, one of the core contributors will review it and give feedback or merge as appropriate.


Asking for Help
---------------

If you need help with something, that's totally fine.
Do what you can and then ask for what you need!
A good place to ask for help is on the issue that you're attempting to tackle; leave a comment with the question that you've got and what you've attempted thus far.
Be aware that there may be a delay before someone comes along who has time to provide assistance.

If you have any questions or want to start contributing, chat with us on Slack_.

.. _Slack: https://slack-djangographapi.now.sh/


Code of conduct
---------------

This project adheres to and supports the `Django Code of Conduct`_.

.. _Django Code of Conduct: https://www.djangoproject.com/conduct/


Style guide
-----------

This project uses the `Django coding style guide`_.

.. _Django coding style guide: https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/
