#!/usr/bin/env python

"""
Copyright (c) 2006-2017 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
import re
import random

def fuzz(payload, **kwargs):
    """
    Add random comments to SQL keywords

    >>> import random
    >>> random.seed(0)
    >>> tamper('INSERT')
    'I/**/N/**/SERT'
    """

    retVal = payload

    if payload:
        for match in re.finditer(r"\b[A-Za-z_]+\b", payload):
            word = match.group()

            if len(word) < 2:
                continue

            if True:
                _ = word[0]

                for i in xrange(1, len(word) - 1):
                    _ += "%s%s" % ("/**/" if random.randint(0, 1) else "", word[i])

                _ += word[-1]

                if "/**/" not in _:
                    index = random.randint(1, len(word) - 1)
                    _ = word[:index] + "/**/" + word[index:]

                retVal = retVal.replace(word, _)

    return retVal
