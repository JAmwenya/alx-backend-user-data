#!/usr/bin/env python3
"""
Filtered Logger for handling sensitive user data.
"""

import re
import logging
import os
from typing import List
import mysql.connector
from mysql.connector.connection import MySQLConnection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Obfuscate specified fields in a log message.
    Args:
        fields (List[str]): Fields to obfuscate.
        redaction (str): Replacement string.
        message (str): Original log message.
        separator (str): Field separator in the message.
    Returns:
        str: Obfuscated log message.
    """
    for field in fields:
        message = re.sub(rf"{field}=[^;]*", f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for logging PII fields.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with PII fields to redact.
        Args:
            fields (List[str]): Fields to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, redacting PII fields.
        Args:
            record (logging.LogRecord): Log record.
        Returns:
            str: Formatted log record.
        """
        original_message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR
        )


def get_logger() -> logging.Logger:
    """
    Create and configure a logger with a RedactingFormatter.
    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    logger.addHandler(stream_handler)
    return logger


def get_db() -> MySQLConnection:
    """
    Connect to the database using environment variables.
    Returns:
        MySQLConnection: Database connection object.
    """
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
    )


def main():
    """
    Retrieve rows from the database and log them with PII redacted.
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users;")
    fields = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        message = "; ".join(f"{field}={value}" for field, value in zip(fields, row))
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
