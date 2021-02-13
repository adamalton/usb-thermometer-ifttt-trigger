
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_DIR=`dirname $DIR`

if [ ! -f "$PROJECT_DIR/data/server_pid" ]; then
	echo "data/server_pid file doesn't exist, so process is probably not running."
else
	PID="$(cat $PROJECT_DIR/data/server_pid)"
	echo "Killing server process ($PID)"
	kill "$PID"
fi
