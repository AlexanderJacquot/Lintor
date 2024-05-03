#! /bin/bash

echo "Linting Python"
python3 -m flake8 './app' ||
if [ "true" == "true" ]; then  # This still needs to be a meaningful condition
  exit 1
fi

echo 'Hello'