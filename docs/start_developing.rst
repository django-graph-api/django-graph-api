
Start developing
================

Clone the Github_ repo
::

    git clone https://github.com/melinath/django-graph-api/

Create and activate a virtualenv for the project.

Install the project and test requirements
::

    pip install -r requirements.txt
    pip install -r requirements-test.txt

To run the sample Star Wars project, run
::

    python django_graph_api/tests/starwars/manage.py runserver

You should be able to see the GraphiQL app and run queries by navigating to ``localhost:8000/graphql``.

To run the tests, run
::

    pytest

.. _Github: https://github.com/melinath/django-graph-api/


Build the docs
--------------

Navigate to the ``docs`` directory,
install the docs requirements,
then build the docs files as html:
::

    cd docs
    pip install -r requirements.txt
    make html

View the docs by opening ``_build/html/index.html`` in your browser.
