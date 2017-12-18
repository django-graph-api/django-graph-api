Django Graph API |travis| |slack| |rtd|
========================================

.. |slack| image:: https://slack-djangographapi.now.sh/badge.svg
   :alt: Join us on slack at https://slack-djangographapi.now.sh
   :target: https://slack-djangographapi.now.sh
.. |travis| image:: https://travis-ci.org/melinath/django-graph-api.svg?branch=master
   :alt: Build status on travis-ci
   :target: https://travis-ci.org/melinath/django-graph-api
.. |rtd| image:: https://readthedocs.org/projects/django-graph-api/badge/?version=latest
   :alt: Docs status on readthedocs
   :target: http://django-graph-api.readthedocs.io/

This is an implementation of GraphQL_ in Python_, designed to work with the
Django_ web framework. The project began at `DjangoCon US 2017`_.

Why Django Graph API?
---------------------

We see GraphQL as a promising alternative to REST.

In order to increase its usage amongst Python developers, we are trying to create a library that stays up to date with the GraphQL specs and that embraces all of the things we love about Python:

- simple, readable, and elegant
- great documentation
- supportive open-source community

.. _GraphQL: http://graphql.org/
.. _Python: https://www.python.org/
.. _Django: https://www.djangoproject.com/
.. _DjangoCon US 2017: https://2017.djangocon.us/

Contributing
------------

We welcome contributions! We use Github projects to organize our ticket workflow. If there's a particular issue you would like to work on and it isn't already assigned, feel free to assign it to yourself and start work! If you just want to lend a hand, check out the current project and choose one of the tickets from the backlog!

Once you're done writing code, you will need to open a pull request with your changes. In order to be merged, pull requests must fulfill the following requirements:

- All new code must have tests.
- All tests must be passing.
- Any relevant documentation has been updated.

If you need help with something, that's totally fine. Do what you can and then ask for what you need! Just be aware that there may be a delay before someone comes along who has time to provide it.

Once your pull request is complete, one of the core contributors will review it and give feedback or merge as appropriate.

To run the tests, run ``pytest``.

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

Documentation
^^^^^^^^^^^^^

You can find the `full documentation <https://django-graph-api.readthedocs.io>`_ for Django Graph API on ReadTheDocs.

To create the docs locally,
navigate to the ``docs`` directory,
install the docs requirements,
then build the docs files as html:
::

   cd docs
   pip install -r requirements.txt
   make html

The resulting ``index.html`` file will be in ``_build/html/``.
