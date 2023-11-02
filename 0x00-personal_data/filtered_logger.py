#!/usr/bin/env python3

"""
Solving filtered logger task
"""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str, separator:
str) -> str:
    """Return obfuscated log message"""
    for field in fields:
        message = re.sub(r'{}[^{}]+'.format(field, separator),
                         field + "=" + redaction + separator, message)
    return message
