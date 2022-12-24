#!/bin/sh

set -e

# TODO: check platform architecture
for dir in $(find . -name "depend_x86_64.sh" | sed -r 's|/[^/]+$||'); do
    cd $dir && ./depend_x86_64.sh && cd ..
done
