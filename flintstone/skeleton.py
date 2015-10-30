#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following line in the
entry_points section in setup.cfg:

    console_scripts =
        hello_world = flintstone.module:function

Then run `python setup.py install` which will install the command `hello_world`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""
from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging

from flintstone import __version__
from curtsies import FullscreenWindow, Input

from .layout_manager import HStackLayout, VStackLayout, OverlayLayout
from .widget import Group, HFill, VFill, Frame

__author__ = "Malte Harder"
__copyright__ = "Malte Harder"
__license__ = "new-bsd"

_logger = logging.getLogger(__name__)

'''
Created on 15.06.15

@author = mharder
'''



def run_ui():
    with FullscreenWindow() as window:
        with Input() as input_generator:
            root = OverlayLayout(window)

            #g1 = Frame(root)

            #menu3 = HFill(g1, height=5)

            g2 = Frame(root, VStackLayout(), border=True, opaque=False, title="Hallo World")

            a = VFill(g2, width=20)
            b = VFill(g2, width=None)
            c = VFill(g2, width=30)

            root.render()

            for c in input_generator:
                if c == u'<ESC>':
                    break
                if c == u't':
                    b.tangible = not b.tangible
                if c == u'v':
                    b.visible = not b.visible
                root.render()

def parse_args(args):
    """
    Parse command line parameters

    :param args: command line parameters as list of strings
    :return: command line parameters as :obj:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="Just a Hello World demonstration")
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='flintstone {ver}'.format(ver=__version__))
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)
    run_ui()


def run():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
