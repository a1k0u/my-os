#!/bin/bash

<< BookExecute
  Starts python script.

  Python address book with ability to insert, search, delete
  and show user's contacts (name, surname, phone,
  email, extra information) in a pretty table,
  which output in stdout.
BookExecute

info="""
    ! Don't forget to change mode to execute.
    ! Make this programme shorter in .bashrc:

        alias book='cd <path>/ && ./book.sh'

    Output information about script (instruction):
    >> book -help

    Shows all table data
    >> book -s

    Enter a new user with the name 'John', phone number '+123456' and extra information.
    >> book -name John -phone +123456 -information 'My favorite character'

    Delete all users with the name 'Alex' and the last name 'Kosenko'.
    >> book -d -name Alex -surname Kosenko

    Search for a user by email and phone.
    >> book -g -phone +77777 -email kooko123@mail.world

    Functions:
        -i : insert into the table
        -s : show table
        -d : delete from the table
        -g : search for users in the table

    Fields:
        - first name, -last name, - phone, -email, -information

    - Flags before data is required.
    - If the data contains more than one word, enclose them in quotation marks.
    - If the execute function is not mentioned, 'get_all' will run.
"""

if [ "$1" == "-help" ]
then
  echo "$info"
else
  path=$(echo "$0" | grep -P -o "\/.*\/")
  cd "$path" && /usr/bin/python3 book.py "$@"
fi
