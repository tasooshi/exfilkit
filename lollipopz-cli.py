#!/usr/bin/env python3

import argparse
import importlib
import logging

import lollipopz as lpz


def class_import(path):
    module_path, _, cls_name = path.rpartition('.')
    path_module = importlib.import_module(module_path)
    clss = getattr(path_module, cls_name)
    return clss


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-d', '--debug', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-v', '--version', action='version', version=lpz.__version__)
    parser.add_argument('-m', '--module', nargs='?', required=True)
    args, _ = parser.parse_known_args()
    handler = class_import(args.module)()
    handler.extra_args(parser)
    args = parser.parse_args()
    lpz.handler.setLevel(args.loglevel)
    lpz.logger.setLevel(args.loglevel)
    lpz.handler.setFormatter(lpz.formatter[args.loglevel])
    handler.init(vars(args))
    handler.execute()
