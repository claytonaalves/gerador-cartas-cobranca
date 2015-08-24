#!/bin/bash
openssl enc -d -a -aes-256-cbc -in environ.enc > environ.sh
if [ $? -eq 0 ]; then
    source environ.sh
fi
