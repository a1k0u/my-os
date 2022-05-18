#!/usr/bin/python3

"""
Script info
"""

from typing import Callable, DefaultDict
from collections import defaultdict
from sys import argv

import sqlite3 as sql
from prettytable import from_db_cursor


def database(command: Callable) -> Callable:
    """

    :param command:
    :return:
    """

    def wrapper(**kwargs) -> None:
        with sql.connect("book.sqlite") as connection:
            command(defaultdict(str, kwargs), cursor=connection.cursor())

    return wrapper


@database
def create_tables(kwargs: DefaultDict, cursor: sql.Cursor = None) -> None:
    """

    :param kwargs:
    :param cursor:
    :return:
    """

    with open("tables.sql", mode="r", encoding="utf-8") as table:
        cursor.executescript(table.read())


@database
def get_user(kwargs: DefaultDict, cursor: sql.Cursor = None) -> None:
    """

    :param kwargs:
    :param cursor:
    :return:
    """

    if not kwargs["name"]:
        ...

    cursor.execute("SELECT * FROM users WHERE name = :name", kwargs)
    print(from_db_cursor(cursor))


@database
def get_all(kwargs: DefaultDict, cursor: sql.Cursor = None) -> None:
    """

    :param kwargs:
    :param cursor:
    :return:
    """

    cursor.execute("SELECT * FROM users")
    print(from_db_cursor(cursor))


@database
def insert_user(kwargs: DefaultDict, cursor: sql.Cursor = None) -> None:
    """

    :param kwargs:
    :param cursor:
    :return:
    """

    if not kwargs["name"]:
        ...

    cursor.execute(
        "INSERT INTO users VALUES (NULL, :name, :surname, :phone, :email, :information)",
        kwargs,
    )


# insert_user(name="John", phone="+7900")
# insert_user(name="Bobi", surname="Huck")
# insert_user(name="Rick", surname="Morty", phone="+7900", email="Ki@ma.e", information="funny")
# get_all()
# get_user(name="Rick")
