#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    from distutils.core import setup
    find_packages = None


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'tendril-utils-core>=0.1.13',
    'tendril-utils-types>=0.1.8',
    'tendril-config>=0.1.6',
    'tendril-schema>=0.1.12',
    'tendril-prototype-base>=0.1.3',
    'tendril-costing>=0.1.2',
    'tendril-pricing>=0.1.8'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='tendril-products',
    version='0.1.16',
    description="Tendril Products Primitives",
    long_description=readme,
    author="Chintalagiri Shashank",
    author_email='shashank@chintal.in',
    url='https://github.com/chintal/tendril-products',
    packages=find_packages(),
    install_requires=requirements,
    license="AGPLv3",
    zip_safe=False,
    keywords='tendril',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    # test_suite='tests',
    # tests_require=test_requirements
)
