#! /usr/bin/env sh
set -e

python3 /app/app/manage.py collectstatic \
          --ignore=node_modules --ignore=.sass-cache       \
          --ignore=*.sass --ignore=*.scss --ignore=*.tsx   \
          --ignore=gulpfile.js --ignore=start.js           \
          --ignore=gulp                                    \
          --ignore=*.ts --ignore=*.jsx --ignore=tsconfig.* \
          --ignore=npm* --ignore=._.DS_Store --ignore=_*   \
          --ignore=package.json --ignore=package-lock.json \
          --ignore=.babelrc --ignore=*.log                 \
          --noinput &> /dev/null

#if [ -f /app/app/administration/wsgi.py ]; then
DEFAULT_MODULE_NAME=administration.asgi
#elif [ -f /app/administration/wsgi.py ]; then
#    DEFAULT_MODULE_NAME=app.administration.asgi:application
#fi

echo $DEFAULT_MODULE_NAME

MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

if [ -f /app/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/app/gunicorn_conf.py
elif [ -f /app/app/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/app/app/gunicorn_conf.py
else
    DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
fi
export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
#export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

# If there's a prestart.sh script in the /app directory or other path specified, run it before starting
PRE_START_PATH=${PRE_START_PATH:-/app/prestart.sh}
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else
    echo "There is no script $PRE_START_PATH"
fi

# Start Gunicorn
exec gunicorn -c "$GUNICORN_CONF" "$APP_MODULE"
