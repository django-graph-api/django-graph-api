
Start developing
================

Set up the project
------------------

1. Clone the Github_ repo
#. Navigate to the ``django-graph-api`` directory
#. Create and activate the project's virtual environment
#. Install the project requirements

If you are using pipenv_:
::

    git clone https://github.com/melinath/django-graph-api/
    cd django-graph-api
    pipenv install    # this will create your virtualenv and install the requirements

Run the tests
-------------

1. Activate the virtualenv
#. Install the test requirements
#. Run the tests

::

    pipenv shell
    pip install -r requirements-test.txt
    pytest

Run the test project
--------------------
Django Graph API comes with a sample Django project
based on the Star Wars examples from the GraphQL documentation.
It is used for integration tests and to help with development.

1. Install the local version of django-graph-api
#. Migrate the db
#. Add some data
#. Start the dev server

While in the root project directory,
in an active virtual environment:
::

    pip install .
    ./manage.py migrate
    ./manage.py shell
    # Add some data
    # django_graph_api/tests/conftest.py has some code you can copy and paste
    ./manage.py runserver

You should be able to see the GraphiQL app and run queries
by navigating to ``localhost:8000/graphql`` in your browser.

.. _Github: https://github.com/melinath/django-graph-api/
.. _pipenv: https://github.com/kennethreitz/pipenv/

Build the docs
--------------

1. Navigate to the ``docs`` directory
#. Install the docs requirements
#. Build the docs files as html

::

    cd docs
    pip install -r requirements.txt
    make html

View the docs by opening ``_build/html/index.html`` in your browser.
