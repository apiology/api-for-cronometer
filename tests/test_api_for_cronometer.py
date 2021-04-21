#!/usr/bin/env python

"""Tests for `api_for_cronometer` package."""

import argparse
import os
import subprocess
from unittest.mock import call, patch

import pytest

from api_for_cronometer._cli import parse_argv, process_args


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_process_args():
    with patch('builtins.print') as mock_print:
        ns = argparse.Namespace()
        setattr(ns, '_', '<fake>')
        out = process_args(ns)

        assert out == 0
        mock_print.assert_has_calls([call('Arguments: <fake>'),
                                     call('Replace this message by putting '
                                          'your code into api_for_cronometer.cli.process_args')])


@pytest.mark.skip(reason="working on main help test first")
def test_parse_argv_run_simple():
    argv = ['api_for_cronometer', 'op1', '123']
    args = parse_argv(argv)
    assert vars(args) == {'operation': 'op1', 'arg1': 123}


def test_cli_update_help():
    request_long_lines = {'COLUMNS': '999', 'LINES': '25'}
    env = {}
    env.update(os.environ)
    env.update(request_long_lines)
    expected_help = """\
usage: api_for_cronometer update-macro-targets [-h] [--energy TARGET_KCALS,MAX_KCALS] \
[--protein TARGET_GRAMS,MAX_GRAMS] [--net-carbs TARGET_GRAMS,MAX_GRAMS] \
[--fat TARGET_GRAMS,MAX_GRAMS]

Update macronutrient targets

optional arguments:
  -h, --help            show this help message and exit
  --energy TARGET_KCALS,MAX_KCALS
                        Energy in (kilo-)calories (target and max, comma separated)
  --protein TARGET_GRAMS,MAX_GRAMS
                        Protein in grams (target and max, comma separated)
  --net-carbs TARGET_GRAMS,MAX_GRAMS
                        Net carbs in grams (target and max, comma separated)
  --fat TARGET_GRAMS,MAX_GRAMS
                        Fat in grams (target and max, comma separated)
"""
    # older python versions show arguments like this:
    actual_help = subprocess.check_output(['api_for_cronometer',
                                           'update-macro-targets',
                                           '--help'],
                                          env=env).decode('utf-8')
    assert actual_help == expected_help


def test_cli_help():
    expected_help = """usage: api_for_cronometer [-h] {update-macro-targets} ...

positional arguments:
  {update-macro-targets}
    update-macro-targets
                        Update macronutrient targets

optional arguments:
  -h, --help            show this help message and exit
"""
    # older python versions show arguments like this:
    alt_expected_help = expected_help.replace('[_ ...]', '[_ [_ ...]]')
    actual_help = subprocess.check_output(['api_for_cronometer', '--help']).decode('utf-8')
    try:
        assert actual_help == expected_help
    except AssertionError:
        assert actual_help == alt_expected_help
