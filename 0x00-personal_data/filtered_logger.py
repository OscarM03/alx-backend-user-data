#!/usr/bin/env python3
"""Personal Data"""

import re
import logging
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection
from typing import List, Tuple

PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """contructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formatting message to filter and return it"""
        msg = super().format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated"""
    prtn = f'({"|".join(fields)})=.*?{separator}'
    return re.sub(prtn, lambda o:
                  f'{o.group(1)}={redaction}{separator}', message)


def get_logger() -> logging.Logger:
    """Creates and set a logger named user_data"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a MySQLConnection object"""
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        user=db_username,
        password=db_pwd,
        host=db_host,
        database=db_name
    )
    return connection


def main():
    """main"""
    connection = get_db()
    if connection is None:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        masked_row = {
            "name": "***",
            "email": "***",
            "phone": "***",
            "ssn": "***",
            "password": "***",
            "ip": row["ip"],
            "last_login": row["last_login"].isoformat(),
            "user_agent": row["user_agent"]
        }
        log_message = "; ".join([f"{key}={value}"
                                 for key, value in masked_row.items()]) + ";"
        logging.info(log_message)

    cursor.close()
    connection.close()
