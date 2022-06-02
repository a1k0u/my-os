"""
Address book with ability to insert, search, delete
and show user's contacts (name, surname, phone,
email, extra information) in a pretty table,
which output in stdout.
"""

from typing import Union, Callable, DefaultDict, Dict, FrozenSet
from collections import defaultdict
from sys import argv

import sqlite3 as sql
from prettytable import from_db_cursor


def create_condition(parameters: DefaultDict) -> str:
    """Creates an SQL condition from Dict."""
    return " AND ".join([f"{key}='{value}'" for key, value in parameters.items()])


def database(command: Callable) -> Callable:
    """
    Python decorator which automate process:
    make a connection to database, execute
    SQL requests, commit and close connection.

    Wrapper takes a dict with arguments for DB.

    :param command: SQL requests in function form.
    :return: wrapper function with automate process.
    """

    def wrapper(parameters: Dict) -> None:
        with sql.connect("book.sqlite") as connection:
            command(connection.cursor(), defaultdict(str, parameters))

    return wrapper


@database
def create_tables(cursor: sql.Cursor, parameters: DefaultDict) -> None:
    """Executes an SQL script to create tables."""
    with open("book_tables.sql", mode="r", encoding="utf-8") as table:
        cursor.executescript(table.read())


@database
def get_user(cursor: sql.Cursor, parameters: DefaultDict) -> None:
    """Finds all users in an SQL table with exact properties."""
    cursor.execute(f"SELECT * FROM users WHERE {create_condition(parameters)}")
    print(from_db_cursor(cursor))


@database
def get_all(cursor: sql.Cursor, parameters: DefaultDict) -> None:
    """Outputs all table in stdout."""
    cursor.execute("SELECT * FROM users")
    print(from_db_cursor(cursor))


@database
def delete_user(cursor: sql.Cursor, parameters: DefaultDict) -> None:
    """Finds all users in a table with properties and deletes them."""
    cursor.execute(f"DELETE FROM users WHERE {create_condition(parameters)}")


@database
def insert_user(cursor: sql.Cursor, parameters: DefaultDict) -> None:
    """Insert user in a table. Fill fields (keys) with values (values) from a dict."""
    cursor.execute(
        """
        INSERT INTO users 
        VALUES 
          (
            NULL, :name, :surname, :phone, :email, 
            :info
          )
        """,
        parameters,
    )


def main() -> None:
    """
    The main function that processes the information entered into the script.
    Check manual in book.sh.
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
    elif function != get_all and not parameters:
        exit("book: fields are empty")

    function(parameters)


if __name__ == "__main__":
    main()
