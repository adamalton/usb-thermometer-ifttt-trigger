set -e

RED='\033[0;31m'
YELLOW='\033[0;93m'
END='\033[0m' # No Color

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_DIR=`dirname $DIR`

function abort {
	echo -e "${RED}${1}. Aborting.${END}"
	exit 1
}

if [ -d "$PROJECT_DIR/.env" ]; then
	rm -r $PROJECT_DIR/.env
fi

if ! command -v virtualenv &> /dev/null; then
	abort "'virtualenv' command doesn't appear to be installed"
fi
if ! command -v python3 &> /dev/null; then
	abort "'python3' command doesn't exist"
fi

virtualenv --python python3 "$PROJECT_DIR/.env"
source $PROJECT_DIR/.env/bin/activate
if ! which pip | grep -q 'env'; then
	abort "Virtualenv didn't seem to activate"
fi
pip install -r "$PROJECT_DIR/requirements.txt"

echo "You now need to run
    $ source .env/bin/activate
to activate the virtualenv."
