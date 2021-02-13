set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_DIR=`dirname $DIR`

source $PROJECT_DIR/.env/bin/activate
nohup python $PROJECT_DIR/djangoapp/manage.py runserver 0.0.0.0:8085 &

DJANGO_SERVER_PROCESS_ID=$!

echo $DJANGO_SERVER_PROCESS_ID

echo "$DJANGO_SERVER_PROCESS_ID" > $PROJECT_DIR/data/server_pid

echo "Started server and wrote process ID ($DJANGO_SERVER_PROCESS_ID) to data/server_pid"
