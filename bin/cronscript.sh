#!/bin/bash

# Script to be called periodically by your crontab.
# Note that you should call this from your root crontab in order for the Python code to have access
# to the USB stuff.


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_DIR=`dirname $DIR`

# Wipe the nohup.out file so that it doesn't get massive.
# I can't see a way to invoke `nohup` and tell it to not append output to that file.
echo "" > $PROJECT_DIR/nohup.out

$PROJECT_DIR/bin/check_server_is_running.sh

$PROJECT_DIR/bin/check_temperature.sh
