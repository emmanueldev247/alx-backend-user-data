#!/usr/bin/env python3
"""
Regex-ing: This module contains functions to securely handle and
           obfuscate sensitive data within log messages.
"""
import re
import logging
from typing import List


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum"""
        return filter_datum(self.fields, RedactingFormatter.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            RedactingFormatter.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Filters a log line"""
    pattern = '|'.join([rf"{field}=([^{separator}]+)" for field in fields])
    return re.sub(pattern,
                  lambda m: f"{m.group().split('=')[0]}={redaction}", message)
