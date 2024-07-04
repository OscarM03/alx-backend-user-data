#!/usr/bin/env python3
"""Personal Data"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated"""
    prtn = f'({"|".join(fields)})=.*?{separator}'
    return re.sub(prtn, lambda o:
                  f'{o.group(1)}={redaction}{separator}', message)
