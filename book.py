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


def create_condition(kwargs: DefaultDict) -> str:
    """
    Creates an SQL condition from Dict.

    :param kwargs: a dict with keys and values.
    :return: the result of concatenating conditions.
    """

    return " AND ".join([f"{key}='{value}'" for key, value in kwargs.items()])


def database(command: Callable) -> Callable:
    """
    Python decorator which automate process:
    make a connection to database, execute
    SQL requests, commit and close connection.

    Wrapper takes a dict with arguments for DB.

    :param command: SQL requests in function form.
    :return: wrapper function with automate process.
    """

    def wrapper(**kwargs) -> None:
        with sql.connect("book.sqlite") as connection:
            command(defaultdict(str, kwargs), cursor=connection.cursor())

    return wrapper


@database
def create_tables(kwargs: DefaultDict, cursor: sql.Cursor = None) -> None:
    """
    Executes an SQL script to create tables.

    :param kwargs: unused in this func, but necessary for polymorphism.
    :param cursor: SQL cursor.
    :return: None
    """

    with open("book_tables.sql", mode="r", encoding="utf-8") as table:
        cursor.executescript(table.read())


@database
def get_user(kwargs: DefaultDict, cursor: sql.Cursor = None) -> None:
    """
    Finds all users in an SQL table
    with exact properties.

    :param kwargs: users parameters.
    :param cursor: SQL cursor.
    :return: output table in stdout.
    """

    cursor.execute(f"SELECT * FROM users WHERE {create_condition(kwargs)}")
    print(from_db_cursor(cursor))


@database
def get_all(kwargs: DefaultDict, cursor: sql.Cursor = None) -> None:
    """
    Outputs all table in stdout.

    :param kwargs: unused in this func, but necessary for polymorphism.
    :param cursor: SQL cursor.
    :return: None
    """

    cursor.execute("SELECT * FROM users")
    print(from_db_cursor(cursor))


@database
def delete_user(kwargs: DefaultDict, cursor: sql.Cursor = None) -> None:
    """
    Finds all users in a table
    with properties and deletes them.

    :param kwargs: users parameters.
    :param cursor: SQL cursor.
    :return: None
    """

    cursor.execute(f"DELETE FROM users WHERE {create_condition(kwargs)}")


@database
def insert_user(kwargs: DefaultDict, cursor: sql.Cursor = None) -> None:
    """
    Insert user in a table. Fill fields (keys)
    with values (values) from a dict.

    :param kwargs: new user parameters.
    :param cursor: SQL cursor.
    :return: None
    """

    cursor.execute(
        """
        INSERT INTO users 
        VALUES 
          (
            NULL, :name, :surname, :phone, :email, 
            :information
          )
        """,
        kwargs,
    )


def main() -> None:
    """
    The main function that processes the information entered into the script.

    Shows all table data (~ `get_all`)
    >> python3 book.py -s

    Enter a new user with the name "John", phone number "+123456" and extra information.
    >> python3 book.py -name John -phone +123456 -information "My favorite character"

    Delete all users with the name "Alex" and the last name "Kosenko".
    >> python3 book.py -d -name Alex -surname Kosenko

    Search for a user by email and phone.
    >> python3 book.py -g -phone +77777 -email kooko123@mail.world

    Functions:
        -i : insert into the table
        -s : show table
        -d : delete from the table
        -g : search for users in the table

    Fields:
        - first name, -last name, - phone, -email, -information

    - Flags before data is required.
    - If the data contains more than one word, enclose them in quotation marks.
    - If the execute function is not mentioned, 'get_all' will run ( ~python3 book.py ).

    :return: None
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
