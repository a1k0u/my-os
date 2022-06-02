#!/bin/bash

<<PermissionDoc
  Finds out what permissions a certain user
  has for a certain file or directory.

  Example:
  > permission.sh someFile.txt root
  > root able to read, write, execute.

  > permission.sh SuperSecretDirectory vasily
  > vasily doesn't have any permission.

  > permission.sh File.py
  > petya able to execute.

  If we don't mentioned user, program will get $LOGNAME.
PermissionDoc

function _get_word_by_num() {
  word=$(echo "$1" | grep -P -o "[\S]+" | head "-$2" | tail -1)
  echo "$word"
}

function get_obj_info() {
  information=$(ls -lad "$1")
  echo "$information"
}

function get_obj_permissions() {
  permissions=$(_get_word_by_num "$1" 1)
  echo "${permissions:1:${#permissions}}"
}

function get_obj_owner() {
  owner=$(_get_word_by_num "$1" 3)
  echo "$owner"
}

function get_obj_group() {
  group=$(_get_word_by_num "$1" 4)
  echo "$group"
}

function _iterate_permissions() {
    start=$1
    for (( i=start; i < start + 3; i++ )); do
      user_permissions[${obj_permissions:i:1}]=1
    done
}

function check_owner_permission() {
  _iterate_permissions 0
}

function check_group_permission() {
  user_groups=$(groups "$user" 2> /dev/null | grep -P -o "(?<=\:).*" | grep -P -o "[\S]+")
  for group in $user_groups; do
    if [ "$group" == "$obj_group" ]; then
      _iterate_permissions 3
      break
    fi
  done
}

function check_others_permission() {
  _iterate_permissions 6
}

function _formatter_output() {
  string=""
  if [ "${user_permissions["r"]}" == "1" ]; then string+="read, "; fi
  if [ "${user_permissions["w"]}" == "1" ]; then string+="write, "; fi
  if [ "${user_permissions["x"]}" == "1" ]; then string+="execute, "; fi

  if [ -z "$string" ]; then
    echo "$user doesn't have any permission."
  else
    echo "$user able to ${string:0:${#string}-2}."
  fi
}

function get_user_obj_permissions() {
  obj=$1; user=$LOGNAME
  if [ -n "$2" ]; then user=$2; fi

  if [ ! -e "$obj" ]; then
    echo "$obj doesn't exist."
    exit
  fi

  obj_info=$(get_obj_info "$obj")
  obj_permissions=$(get_obj_permissions "$obj_info")
  obj_owner=$(get_obj_owner "$obj_info")
  obj_group=$(get_obj_group "$obj_info")

  declare -A user_permissions=(["r"]=0 ["w"]=0 ["x"]=0 ["-"]=0)
  if [ "$obj_owner" == "$user" ]; then
    check_owner_permission
  else
    check_others_permission
  fi
  check_group_permission

  result=$(_formatter_output)
  echo "$result"
}


test=$(get_user_obj_permissions "ip-info.sh")
echo "$test"
