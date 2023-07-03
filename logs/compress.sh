#!/bin/bash
# Compresses all logs even densier and removes originals

gzip -d *.log.gz
tar -caf logs.tar.gz *.log --remove-files --backup=simple