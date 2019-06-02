#!/usr/bin/env bash

if [[ $1 == "build" ]]; then
    rm -rf ./dist/
    python setup.py sdist bdist_wheel
elif [[ $1 == "publish" ]]; then
    twine upload dist/*
else
    echo "run 'build.sh build' or 'build.sh publish'"
fi

