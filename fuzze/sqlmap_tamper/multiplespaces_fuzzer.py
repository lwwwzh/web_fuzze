#!/usr/bin/env python

"""
Copyright (c) 2006-2017 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

import random
import re


def fuzz(payload, **kwargs):
    """
    Adds multiple spaces around SQL keywords

    Notes:
        * Useful to bypass very weak and bespoke web application firewalls
          that has poorly written permissive regular expressions

    Reference: https://www.owasp.org/images/7/74/Advanced_SQL_Injection.ppt

    >>> random.seed(0)
    >>> tamper('1 UNION SELECT foobar')
    '1    UNION     SELECT   foobar'
    """

    retVal = payload

    if payload:
        words = set()

        for match in re.finditer(r"[A-Za-z_]+", payload):
            word = match.group()

            words.add(word)

        for word in words:
            retVal = re.sub("(?<=\W)%s(?=[^A-Za-z_(]|\Z)" % word, "%s%s%s" % (' ' * random.randrange(1, 4), word, ' ' * random.randrange(1, 4)), retVal)
            retVal = re.sub("(?<=\W)%s(?=[(])" % word, "%s%s" % (' ' * random.randrange(1, 4), word), retVal)

    return retVal
