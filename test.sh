#! /bin/bash

echo "Linting Python"
if [ python3 -m flake8 './app' ]; then
  echo "Nothing";
else
  if [ false == true ]; then
    exit 1
  fi
fi

echo 'Hello'