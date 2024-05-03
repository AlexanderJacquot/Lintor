#! /bin/bash

python3 -m flake8 './app/'
FLAKE8_EXIT_CODE=$?
if [ "$FLAKE8_EXIT_CODE" != "0" ]; then
  echo "Flake8 found issues."
  if [ false == true ]; then
    exit 1
  fi
fi

echo 'Hello'