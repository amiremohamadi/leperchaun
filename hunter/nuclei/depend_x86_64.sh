#!/bin/sh

set -e

wget https://github.com/projectdiscovery/nuclei/releases/download/v2.7.0/nuclei_2.7.0_linux_amd64.zip
unzip nuclei_2.7.0_linux_amd64.zip
./nuclei
