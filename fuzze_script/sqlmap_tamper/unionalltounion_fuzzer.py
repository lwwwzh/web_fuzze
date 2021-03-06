#!/usr/bin/env python

"""
Copyright (c) 2006-2017 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

def fuzz(payload, **kwargs):
    """
    Replaces UNION ALL SELECT with UNION SELECT

    >>> tamper('-1 UNION ALL SELECT')
    '-1 UNION SELECT'
    """

    return payload.replace("UNION ALL SELECT", "UNION SELECT") if payload else payload
