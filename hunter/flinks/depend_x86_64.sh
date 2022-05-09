#!/bin/sh

set -e

wget https://github.com/jaeles-project/gospider/releases/download/v1.1.6/gospider_v1.1.6_linux_x86_64.zip
unzip gospider_v1.1.6_linux_x86_64.zip && cp gospider_v1.1.6_linux_x86_64/gospider . && rm -rf gospider_v1.1.6_linux_x86_64/
