#!/usr/bin/env python

"""Tests for `api-for-cronometer` package."""

import argparse
import io
import os
import subprocess
import sys
from unittest.mock import call, patch

import pytest

import api_for_cronometer
from api_for_cronometer._cli import main, parse_argv, process_args


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_dunders(response):
    assert api_for_cronometer.__author__ is not None
    assert api_for_cronometer.__email__ is not None
    assert api_for_cronometer.__version__ is not None


@patch('builtins.print', autospec=print)
def test_process_args(print):
    ns = argparse.Namespace()
    setattr(ns, 'foo', '<fake>')
    out = process_args(ns)

    assert out == 0
    print.assert_has_calls([call("Arguments: Namespace(foo='<fake>')"),
                            call('Replace this message by putting '
                                 'your code into api_for_cronometer.cli.process_args')])


@pytest.mark.skip(reason="working on main help test first")
def test_parse_argv_run_simple():
    argv = ['api-for-cronometer', 'op1', '123']
    args = parse_argv(argv)
    assert vars(args) == {'operation': 'op1', 'arg1': 123}


@patch('sys.stderr', new_callable=io.StringIO)
def test_parse_argv_show_args_when_no_options_given_to_update_macro_targets(stderr):
    argv = ['api-for-cronometer', 'update-macro-targets']
    with pytest.raises(SystemExit):
        parse_argv(argv)
    assert 'update-macro-targets [-h]' in stderr.getvalue()
    assert 'error: Please provide an argument to update-macro-targets' in stderr.getvalue()


@patch('api_for_cronometer._cli.parse_argv', autospec=parse_argv)
@patch('api_for_cronometer._cli.process_args', autospec=process_args)
def test_main(process_args, parse_argv):
    argv = object()
    args = parse_argv.return_value
    assert process_args.return_value == main(argv)
    process_args.assert_called_with(args)


def test_cli_update_help():
    request_long_lines = {'COLUMNS': '999', 'LINES': '25'}
    env = {}
    env.update(os.environ)
    env.update(request_long_lines)
    expected_help = """\
usage: api-for-cronometer update-macro-targets [-h] [--energy TARGET_KCALS,MAX_KCALS] \
[--protein TARGET_GRAMS,MAX_GRAMS] [--net-carbs TARGET_GRAMS,MAX_GRAMS] \
[--fat TARGET_GRAMS,MAX_GRAMS]

Update macronutrient targets

options:
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
    if sys.version_info <= (3, 10):
        # 3.10 changed the wording a bit
        expected_help = expected_help.replace('options:', 'optional arguments:')
    # older python versions show arguments like this:
    actual_help = subprocess.check_output(['api-for-cronometer',
                                           'update-macro-targets',
                                           '--help'],
                                          env=env).decode('utf-8')
    assert actual_help == expected_help


def test_cli_no_command():
    request_long_lines = {'COLUMNS': '999', 'LINES': '25'}
    env = {}
    env.update(os.environ)
    env.update(request_long_lines)
    expected_help = """usage: api-for-cronometer [-h] {update-macro-targets} ...
api-for-cronometer: error: Please provide a command
"""
    result = subprocess.run(['api-for-cronometer'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            env=env)
    actual_help = result.stderr.decode('utf-8')
    assert actual_help == expected_help


def test_cli_help():
    expected_help = """usage: api-for-cronometer [-h] {update-macro-targets} ...

positional arguments:
  {update-macro-targets}
    update-macro-targets
                        Update macronutrient targets

options:
  -h, --help            show this help message and exit
"""
    if sys.version_info <= (3, 10):
        # 3.10 changed the wording a bit
        expected_help = expected_help.replace('options:', 'optional arguments:')
    actual_help = subprocess.check_output(['api-for-cronometer', '--help']).decode('utf-8')
    assert actual_help == expected_help
