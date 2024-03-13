#!/bin/bash
echo off
set -e

echo "Running tests..."
python test/test.py
echo
echo "Tests passed, running main application..."
echo
echo
exec python main.py