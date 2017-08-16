#!/usr/bin/env python

"""
Copyright (c) 2006-2017 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

import re


def fuzz(payload, **kwargs):
    """
    Replaces all occurances of operator equal ('=') with operator 'LIKE'

    Tested against:
        * Microsoft SQL Server 2005
        * MySQL 4, 5.0 and 5.5

    Notes:
        * Useful to bypass weak and bespoke web application firewalls that
          filter the equal character ('=')
        * The LIKE operator is SQL standard. Hence, this tamper script
          should work against all (?) databases

    >>> tamper('SELECT * FROM users WHERE id=1')
    'SELECT * FROM users WHERE id LIKE 1'
    """

    retVal = payload

    if payload:
        retVal = re.sub(r"\s*=\s*", " LIKE ", retVal)

    return retVal
