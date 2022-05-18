#!/usr/bin/python3

"""
Script info
"""

from typing import Union, Callable, DefaultDict, Dict, FrozenSet
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
def delete_user(kwargs: DefaultDict, cursor: sql.Cursor = None) -> None:
    """

    :param kwargs:
    :param cursor:
    :return:
    """

    condition = " AND ".join([f"{key}='{value}'" for key, value in kwargs.items()])
    cursor.execute(f"DELETE FROM users WHERE {condition}")


@database
def insert_user(kwargs: DefaultDict, cursor: sql.Cursor = None) -> None:
    """

    :param kwargs:
    :param cursor:
    :return:
    """

    cursor.execute(
        "INSERT INTO users VALUES (NULL, :name, :surname, :phone, :email, :info)",
        kwargs,
    )


def main() -> None:
    """

    :return:
    """

    functions: Dict[str, Callable] = {
        "-i": insert_user,
        "-g": get_user,
        "-s": get_all,
        "-d": delete_user,
    }

    fields: FrozenSet[str] = frozenset(
        ("-name", "-surname", "-phone", "-email", "-info")
    )

    flag: bool = False
    parameters: Dict[str, str] = {}
    function: Union[None, Callable] = None

    for i in range(1, len(argv)):
        if flag:
            flag = False
            parameters[argv[i - 1][1:]] = argv[i]
        elif function is None and functions.get(argv[i], None) is not None:
            function = functions[argv[i]]
        elif argv[i] in fields:
            flag = True
        else:
            exit(f"book: invalid input `{argv[i]}`")

    if function is None:
        function = get_all
    elif function != get_all:
        if parameters.get("name", None) is None:
            exit("book: field `name` is empty")

    function(**parameters)


if __name__ == "__main__":
    main()
