#!/bin/bash

set -e

docker stop jass-2024-assignment-limarkdl || true && docker rm jass-2024-assignment-limarkdl || true

docker build --no-cache -t jass-2024-limarkdl .
# shellcheck disable=SC2046
# shellcheck disable=SC2005
echo $(pwd)
# shellcheck disable=SC2046
docker run -it --name jass-2024-assignment-limarkdl -v $(pwd):/task2/ jass-2024-limarkdl
# shellcheck disable=SC2046
xdg-open $(pwd)/output.png
