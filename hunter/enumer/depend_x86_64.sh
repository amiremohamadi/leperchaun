#!/bin/sh

set -e

wget https://github.com/tomnomnom/assetfinder/releases/download/v0.1.1/assetfinder-linux-amd64-0.1.1.tgz
tar xf assetfinder-linux-amd64-0.1.1.tgz

wget https://github.com/projectdiscovery/subfinder/releases/download/v2.5.1/subfinder_2.5.1_linux_amd64.zip
unzip subfinder_2.5.1_linux_amd64.zip
