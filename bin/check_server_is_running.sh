#!/bin/bash

# Checks if the web server (which allows easy changing of settings) is running, and if it's not
# then starts it.

# This should be called periodically by a cron job.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_DIR=`dirname $DIR`


URL="http://localhost:8085/ping/"
response=$(curl -s -w "\n%{http_code}" $URL)
status_code=$(tail -n1 <<< "$response")  # get the last line

if [[ $status_code != "200" ]]; then
	echo "Server is not running (status code: $status_code). Starting..."
	$PROJECT_DIR/bin/start_server.sh &
else
	PID="$(cat $PROJECT_DIR/data/server_pid)"
	echo "Server is already running (process ID: $PID)"
fi
