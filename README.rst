Django Graph API
================

This is an implementation of GraphQL_ in Python_, designed to work with the
Django_ web framework. The project began at `DjangoCon US 2017`_.

Why Not Graphene?
-----------------

Graphene_ is the standard Python implementation of GraphQL, and it is far more
mature than Django Graph API. So why should you use this project instead of
Graphene?

* Django Graph API is **Pythonic**, while Graphene was ported over from Node.js
  and follows Javascript idioms.

.. _GraphQL: http://graphql.org/
.. _Python: https://www.python.org/
.. _Django: https://www.djangoproject.com/
.. _DjangoCon US 2017: https://2017.djangocon.us/
.. _Graphene: http://graphene-python.org/

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

If you have any questions or want to start contributing, chat with us on gitter_.

.. _gitter: https://gitter.im/django-graph-api/Lobby

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

To create the docs locally, go to the ``docs`` directory, install the requirements, and run ``make html``.

The resulting ``index.html`` file will be in ``_build/html/``.
