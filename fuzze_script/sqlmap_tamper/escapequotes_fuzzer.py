#!/usr/bin/env python

"""
Copyright (c) 2006-2017 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""


def fuzz(payload, **kwargs):
    """
    Slash escape quotes (' and ")

    >>> tamper('1" AND SLEEP(5)#')
    '1\\\\" AND SLEEP(5)#'
    """

    return payload.replace("'", "\\'").replace('"', '\\"')
