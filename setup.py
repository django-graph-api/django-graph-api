#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import django_graph_api


setup(
    name='django-graph-api',
    version=django_graph_api.__version__,
    description='A Python implementation of GraphQL designed for use with Django',
    long_description=open('README.rst', 'r').read(),
    license=open('LICENSE', 'r').read(),
    url='https://github.com/melinath/django-graph-api',
    zip_safe=False,
    packages=find_packages(),
    install_requires=(
        'graphql-py>=0.6',
    ),
    setup_requires=(
        'pytest-runner',
    ),
    tests_require=(
        'pytest',
        'pytest-django',
    ),
    classifiers=(
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django :: 1.11',
    ),
)
