.. django-graph-api documentation master file, created by
   sphinx-quickstart on Tue Sep 12 13:37:37 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django Graph API documentation
============================================
|travis| |gitter|

.. |gitter| image:: https://badges.gitter.im/django-graph-api/Lobby.svg
   :alt: Join the chat at https://gitter.im/django-graph-api/Lobby
   :target: https://gitter.im/django-graph-api/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |travis| image:: https://travis-ci.org/melinath/django-graph-api.svg?branch=master
   :alt: Build status on travis-ci
   :target: https://travis-ci.org/melinath/django-graph-api

`**Django Graph API**`_ lets you quickly build GraphQL_ APIs in Python_. It is designed to work with the Django_ web framework.

What is GraphQL?
----------------

GraphQL is an API query language created by Facebook in 2012 and open-sourced in 2015. Some of its benefits over REST are:

- getting the data you need and nothing more
- getting nested fields without extra requests
- strong typing

For example, if you wanted to get your name and birthday, and the names and birthdays of all of your friends, you could query an API like this:
::

   POST http://myapp/graphql
   "{
       me {
           name
           birthday
           friends {
               name
               birthday
           }
       }
   }"

And an example JSON response would be:
::

   {
      "me": {
         "name": "Buffy Summers",
         "birthday": "1981-01-19",
         "friends": [
            {
               "name": "Willow Rosenberg",
               "birthday": "1981-08-01"
            },
            {
               "name": "Xander Harris",
               "birthday": null
            }
         ]
      }
   }

For an full introduction to GraphQL, you can read the `official documentation`_.

If you have a Github account, you can try out their `GraphQL API explorer`_.

Why Django Graph API?
---------------------

We see GraphQL as a promising alternative to REST.

In order to increase its usage amongst Python developers, we are trying to create a library that stays up to date with the GraphQL specs and that embraces all of the things we love about Python:

- simple, readable, and elegant
- great documentation
- supportive open-source community

If you'd like to help contribute_, read our contributing guidelines and chat with us on Gitter_.

.. _GraphQL: http://graphql.org/
.. _official documentation: http://graphql.org/learn/
.. _Django: https://www.djangoproject.com/
.. _Python: https://www.python.org/
.. _GraphQL API explorer: https://developer.github.com/v4/explorer/
.. _Gitter: https://gitter.im/django-graph-api/Lobby
.. _contribute: contribute.html
.. _**Django Graph API**: https://github.com/melinath/django-graph-api

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   getting_started
   define_nodes

.. toctree::
   :maxdepth: 2
   :caption: Reference Documentation


.. toctree::
   :maxdepth: 1
   :caption: Developer Documentation

   contribute
