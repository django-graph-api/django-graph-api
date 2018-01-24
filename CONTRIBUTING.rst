Contribution Guidelines
=======================

We use `Github projects`_ to organize our ticket workflow.
If you want to lend a hand, check out the current project and choose one of the tickets from the issues!
If there's `a particular issue`_ you would like to work on and it isn't already assigned, leave a comment on that issue indicating your desire to work on it.
Then, start working!

Start Developing
----------------

To get started with your contribution, fork this project into your own GitHub profile and clone that forked repository to your machine.
After cloning, navigate into the new directory and set the original project repository as the remote named ``upstream``.

.. code-block::

    $ cd django-graph-api
    $ git remote add upstream https://github.com/melinath/django-graph-api.git

We're using `pipenv`_ as the package and environment manager for this project.
If you don't yet have it, check the link above for instructions on how to get it on your machine.

Create a ``pipenv`` virtual environment using Python 3.6.
**Note: any code that you write should be compatible with Python 2.7, but we recommend that you develop in Python 3.6.**
``pipenv`` install the ``requirements.txt``, then ``pipenv`` the requirements for testing.

.. code-block::

    $ pipenv install --python 3.6
    $ pipenv install $(< requirements.txt)
    $ pipenv install $(< requirements-test.txt)

Verify that the existing tests pass with ``pipenv run pytest``.

After you see that those tests pass, you can get to work!
Activate the virtual environment that pipenv set up for you and apply the existing migrations.

.. code-block::

    $ pipenv shell # <-- activates the environment
    $ ./manage.py migrate

You should be able to see the GraphiQL app and run queries by navigating to ``localhost:8000/graphql`` in your browser.

Continue to verify that the tests that you write for your code (as well as the existing tests) pass as you develop by simply typing ``pytest``.


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

.. _Github projects: https://github.com/melinath/django-graph-api/projects/4
.. _a particular issue: https://github.com/melinath/django-graph-api/issues
.. _pipenv: https://github.com/pypa/pipenv
.. _Slack: https://slack-djangographapi.now.sh/
