#!/usr/bin/env python2.7

# python2 is used because the python3 (3.5) version of lxml that I tried had
# what I think is a bug: no matter what combination of encoding or other
# parameters I tried, a tree's .write() method would not work on `sys.stdout`.
# It looks like it might work only on file names in the python3 version,
# despite the documentation.

import argparse
import sys
import lxml.etree

parser = argparse.ArgumentParser(
    description='Remove elements from XML (stdin -> stdout).')

parser.add_argument('--no-declaration', action='store_true',
                    help='omit XML declaration')

parser.add_argument('xpath', nargs='*',
                    help='XPath query whose matches will be removed')

options = parser.parse_args()

tree = lxml.etree.parse(sys.stdin)

for xpath_query in options.xpath:
    for element in tree.xpath(xpath_query):
        # We're going to remove the element, but doing so will remove any
        # whitespace after the element and before the next tag (its "tail").
        # So, first replace the previous element's tail with the tail that is
        # about to be removed with the element.
        left_sibling = element.getprevious()
        if left_sibling is not None:
            left_sibling.tail = element.tail

        element.getparent().remove(element)

tree.write(sys.stdout,
           encoding='UTF-8',
           xml_declaration=(not options.no_declaration))
