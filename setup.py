#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script."""

from typing import List

from setuptools import find_packages, setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements: List[str] = []

setup_requirements: List[str] = ['pytest-runner']

test_requirements: List[str] = ['pytest>=3']


setup(
    author="Vince Broz",
    author_email='vince@broz.cc',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Unofficial API CLI/bindings for Cronometer",  # noqa: E501
    entry_points={
        'console_scripts': [
            'api_for_cronometer=api_for_cronometer.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='api_for_cronometer',
    name='api_for_cronometer',
    packages=find_packages(include=['api_for_cronometer',
                                    'api_for_cronometer.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/apiology/api_for_cronometer',
    version='0.1.0',
    zip_safe=False,
)
