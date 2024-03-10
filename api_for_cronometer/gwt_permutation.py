import argparse

from . import gwtmap
from .gwtmap import (BASE_URL, BOOTSTRAP, check_warnings, clean_code,
                     fetch_code, get_permutation, present_target, read_file,
                     set_base_url, set_globals, set_http_params)


def gwt_permutation() -> str:
    args = argparse.Namespace()
    args.url = 'https://cronometer.com/cronometer/cronometer.nocache.js'
    args.file = None
    args.base = BASE_URL
    args.proxy = None
    args.cookies = None
    args.filter = ""
    args.basic = False
    args.rpc = False
    args.probe = False
    args.svc = False
    args.code = False
    args.backup = False
    args.quiet = False

    set_base_url(args.url)

    set_http_params(args)

    print('a')

    if not args.code and not args.quiet:
        present_target(args.url if args.file is None else args.file)

    print('b')

    code, code_type = (
        read_file(args.file) if args.file is not None else
        fetch_code(args.url)
    )

    print('c')

    check_warnings(code_type, args)

    print('d')

    code = clean_code(code, code_type)

    print('e')

    print('Getting permutation')
    if code_type.startswith(BOOTSTRAP) and args.file is None:
        code = get_permutation(code, code_type, args)
    set_globals(code, args)
    print("Permutation fetched: ", gwtmap.GWT_PERMUTATION)
    return gwtmap.GWT_PERMUTATION
