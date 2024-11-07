#!/usr/bin/env python3
"""
Regex-ing: This module contains functions to securely handle and
           obfuscate sensitive data within log messages.
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Filters a log line"""
    pattern = '|'.join([rf"{field}=([^{separator}]+)" for field in fields])
    return re.sub(pattern,
                  lambda m: f"{m.group().split('=')[0]}={redaction}", message)
