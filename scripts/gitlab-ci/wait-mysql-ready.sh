#!/bin/bash

set -e

CHECK_READY_CMD="mysql --host=127.0.0.1 --user=root --password=secret nike -e 'select now();' &> /dev/null"
i=1

if [ ! "$(which mysql)" ]; then
  CHECK_READY_CMD="sleep 30 && nc -vz localhost 3306 &> /dev/null"
fi

if ! eval "$CHECK_READY_CMD"; then
  echo 'Wait for MySQL'
  NL="\n"
fi
while true; do
  if eval "$CHECK_READY_CMD"; then
    echo -e "$NL""MySQL is ready"
    break
  fi
  if [ $i -gt 120 ]; then
    echo -e "\nWait for MySQL timeout"
    exit 1
    break
  fi
  echo -en "."
  sleep 1
  ((i++))
done
