#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

import django_graph_api

here = os.path.abspath(os.path.dirname(__file__))


class UploadCommand(Command):
    """
    Support setup.py upload.

    To use this, you must first:
    $ pip install twine
    """

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name='django-graph-api',
    version=django_graph_api.__version__,
    description='A Python implementation of GraphQL designed for use with Django',
    long_description=open('README.rst', 'r').read(),
    author='Stephen Burrows',
    author_email='stephen.r.burrows@gmail.com',
    url='http://django-graph-api.readthedocs.io/',
    download_url='https://github.com/django-graph-api/django-graph-api',
    zip_safe=False,
    packages=find_packages(exclude=(
        'test_app',
        'test_app.*',
        'test_project',
        'test_project.*',
    )),
    include_package_data=True,
    install_requires=(
        'django>=1.8',
        'graphql-py>=0.6',
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django :: 1.11',
    ),
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
