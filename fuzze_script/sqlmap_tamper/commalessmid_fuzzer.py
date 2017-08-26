#!/usr/bin/env python

"""
Copyright (c) 2006-2017 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

import re


def fuzz(payload, **kwargs):
    """
    Replaces instances like 'MID(A, B, C)' with 'MID(A FROM B FOR C)'

    Requirement:
        * MySQL

    Tested against:
        * MySQL 5.0 and 5.5

    >>> tamper('MID(VERSION(), 1, 1)')
    'MID(VERSION() FROM 1 FOR 1)'
    """

    retVal = payload

    match = re.search(r"(?i)MID\((.+?)\s*,\s*(\d+)\s*\,\s*(\d+)\s*\)", payload or "")
    if match:
        retVal = retVal.replace(match.group(0), "MID(%s FROM %s FOR %s)" % (match.group(1), match.group(2), match.group(3)))

    return retVal
