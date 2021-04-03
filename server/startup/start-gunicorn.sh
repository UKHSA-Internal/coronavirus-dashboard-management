#! /usr/bin/env sh
set -e

python3 $PYTHONPATH/manage.py collectstatic \
          --ignore=node_modules --ignore=.sass-cache       \
          --ignore=*.sass --ignore=*.scss --ignore=*.tsx   \
          --ignore=gulpfile.js --ignore=start.js           \
          --ignore=gulp                                    \
          --ignore=*.ts --ignore=*.jsx --ignore=tsconfig.* \
          --ignore=npm* --ignore=._.DS_Store --ignore=_*   \
          --ignore=package.json --ignore=package-lock.json \
          --ignore=.babelrc --ignore=*.log                 \
          --noinput &> /dev/null

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
export GUNICORN_CONF=${_GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}

echo "Starting Gunicorn with $GUNICORN_CONF on $APP_MODULE"
# Start Gunicorn
exec gunicorn -c "$GUNICORN_CONF" "$APP_MODULE"
