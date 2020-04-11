#!/usr/bin/env bash

# Exit immediately if command fails:
#     https://stackoverflow.com/a/19622569/1717320
set -e

# Print a trace of all commands
set -x

# Install mininet
git clone git://github.com/mininet/mininet
cd mininet
git checkout -b 2.3.0d6 2.3.0d6
cd ..
./mininet/util/install.sh -a