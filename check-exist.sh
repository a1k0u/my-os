#!/bin/bash

<< FindDoc
  This script checks whether any object exists in the system
  or not. If it exists, the program will output the type and
  absolute path to the object.

  Input:
    param dir: relative or absolute path for place,
               where we are going to search.
    param obj: the file or directory we are trying to find.

    example:
      ./someDir
      *myfile.*sh?

      /home
      what?folder
FindDoc


read -rp "Where are we going to search?: " dir
read -rp "What are we going to search?: " obj

if ! [ -e "$dir" ]
then
  echo "Search directory doesn't exist!"
  exit
fi

objects=$(find "$dir" -name "$obj")
echo "$objects"
if [ ${#objects} -eq 0 ]; then
  echo "No objs with label=$obj in directory=$dir !"
else
  index=$((1))

  for object in $objects; do
    type=dir

    if [ -f "$object" ]; then type="file"; fi
    echo "$index. type=$type, path=$(readlink -f "$object")"

    index=$((index + 1))
  done
fi
