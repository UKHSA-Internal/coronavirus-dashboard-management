FROM node:14-buster-slim AS builder
LABEL maintainer="Pouria Hadjibagheri <Pouria.Hadjibagheri@phe.gov.uk>"

WORKDIR /app/static_private

COPY ./app/static_private/css           /app/static_private/css

WORKDIR /app/static_private/css
RUN rm -rf node_modules
RUN npm install
RUN npm rebuild node-sass
RUN npm run build
RUN rm -rf node_modules


FROM python:3.9-buster
LABEL maintainer="Pouria Hadjibagheri <Pouria.Hadjibagheri@phe.gov.uk>"

# Gunicorn binding port
ENV GUNICORN_PORT 5001

ENV PYTHONPATH            /app/app
ENV CSS_PATH              $PYTHON_PATH/static_private/css
ENV DEFAULT_MODULE_NAME   administration.asgi

# ----------------------------------------------------------------------------------------
# Startup scripts - copied from `./server/startup/`
# ----------------------------------------------------------------------------------------
ENV ENTRYPOINT             entrypoint.sh
ENV START_GUNICORN         start-gunicorn.sh
ENV RELOAD                 start-reload.sh

# ----------------------------------------------------------------------------------------
# Configurations - copied from `./server/config/`
# ----------------------------------------------------------------------------------------
ENV GUNICORN_CONF         gunicorn_conf.py
ENV SUPERVISOR_CONF       supervisord.conf
# Do not include `.py` extension for Uvicorn
ENV UVICORN_CONF          uvicorn_worker

# ----------------------------------------------------------------------------------------
# Supervisor configurations
# ----------------------------------------------------------------------------------------
ENV _RUNTIME_CONF_PATH     /opt
ENV _SUPERVISOR_PATH       $_RUNTIME_CONF_PATH/supervisor
ENV _SUPERVISOR_CONF_FILE  $_SUPERVISOR_PATH/$SUPERVISOR_CONF

# ----------------------------------------------------------------------------------------
# Uvicorn configurations
# ----------------------------------------------------------------------------------------
# Uvicorn worker class
ENV _WORKER_CLASS_NAME     APIUvicornWorker
# Import path
ENV _WORKER_CLASS          $UVICORN_CONF.$_WORKER_CLASS_NAME
ENV _WORKER_CLASS_PATH     $PYTHONPATH/$UVICORN_CONF.py

# ----------------------------------------------------------------------------------------
# Gunicorn config
# ----------------------------------------------------------------------------------------
ENV _GUNICORN_CONF         $_RUNTIME_CONF_PATH/gunicorn/$GUNICORN_CONF
ENV _START_GUNICORN        $_RUNTIME_CONF_PATH/gunicorn/$START_GUNICORN

# ----------------------------------------------------------------------------------------
# Ngnix configurations - copied from `./server/ngnix/`
# ----------------------------------------------------------------------------------------
ENV _NGINX_RUNTIME_NAME   hosts.nginx
ENV _NGINX_BASE_PATH      /etc/nginx
ENV _NGINX_BASE_CONF      $_NGINX_BASE_PATH/conf.d
ENV _NGINX_RUNTIME_CONF   $_RUNTIME_CONF_PATH/nginx/$_NGINX_RUNTIME_NAME

# ----------------------------------------------------------------------------------------
# Installation scripts - copied from `./server/installation/`
# ----------------------------------------------------------------------------------------
ENV _INSTALLATION         $_RUNTIME_CONF_PATH/installation        
ENV _NGINX_INSTALLATION   $_INSTALLATION/install-nginx.sh

# ----------------------------------------------------------------------------------------
# Prestart scripts - copied from `./server/prestart/`
# ----------------------------------------------------------------------------------------
ENV PRESTART_INITIATOR     prestart.sh

ENV _CUSTOM_PRESTART_PATH  $_RUNTIME_CONF_PATH/prestart
ENV _PRESTART_SCRIPT       $_CUSTOM_PRESTART_PATH/$PRESTART_INITIATOR

# Adding user + group
RUN addgroup --system --gid 102 app                                  && \
    adduser  --system --disabled-login --ingroup app                    \
             --no-create-home --home /nonexistent                       \
             --gecos "app user" --shell /bin/false --uid 102 app

# Updating the OS + installing supervisor
RUN apt-get update                                                   && \
    apt-get upgrade -y --no-install-recommends --no-install-suggests && \
    apt-get install -qy build-essential --no-install-recommends      && \
    apt-get install -y --no-install-recommends supervisor            && \
    rm -rf /var/lib/apt/lists/*

# Installing Nginx
COPY server/installation/install-nginx.sh   $_NGINX_INSTALLATION

RUN bash $_NGINX_INSTALLATION             && \
    rm /etc/nginx/conf.d/default.conf

# Installing Python requirements
COPY ./requirements.txt                     $_INSTALLATION/requirements.txt

RUN python3 -m pip install --no-cache-dir -U pip                                && \
    python3 -m pip install --no-cache-dir setuptools                            && \
    python3 -m pip install -U --no-cache-dir -r $_INSTALLATION/requirements.txt

# Nginx configurations
COPY server/nginx/base.nginx                $_NGINX_BASE_PATH/nginx.conf
COPY server/nginx/upload.nginx              $_NGINX_BASE_CONF/upload.conf
COPY server/nginx/engine.nginx              $_NGINX_BASE_CONF/engine.conf
COPY server/nginx/hosts.nginx               $_NGINX_RUNTIME_CONF

# Gunicorn configurations
COPY server/config/$GUNICORN_CONF           $_GUNICORN_CONF
COPY server/startup/start-gunicorn.sh       $_START_GUNICORN
RUN chmod +x $_START_GUNICORN

# Supervisor configurations
COPY server/config/$SUPERVISOR_CONF         $_SUPERVISOR_CONF_FILE

# Main service entrypoint - launches supervisord
COPY server/startup/entrypoint.sh           $_RUNTIME_CONF_PATH/$ENTRYPOINT
RUN chgrp app $_RUNTIME_CONF_PATH/$ENTRYPOINT
RUN chmod g+x $_RUNTIME_CONF_PATH/$ENTRYPOINT

# Launch scripts
COPY server/prestart/                       $_CUSTOM_PRESTART_PATH/
RUN chgrp app $_CUSTOM_PRESTART_PATH
RUN chmod +x $_PRESTART_SCRIPT
RUN mkdir -p /app/app

RUN mkdir -p /run/supervisord/                      && \
    mkdir -p $_RUNTIME_CONF_PATH/log/               && \
    mkdir -p $_RUNTIME_CONF_PATH/gunicorn/          && \
    mkdir -p $_RUNTIME_CONF_PATH/nginx/cache/       && \
    chgrp -R app /var/cache/nginx/                  && \
    chmod -R g+rw /var/cache/nginx/                 && \
    chgrp -R app /app/                              && \
    chmod -R g+r /app/                              && \
    chgrp -R app $_RUNTIME_CONF_PATH/               && \
    chmod -R g+wr $_RUNTIME_CONF_PATH/

RUN rm -rf $_INSTALLATION

# Copying built styles
COPY app/                                      $PYTHONPATH/
COPY --from=builder /app/static_private/css    $CSS_PATH
COPY server/config/uvicorn_worker.py           $_WORKER_CLASS_PATH


USER app

EXPOSE 5000

ENTRYPOINT ["/bin/bash", "/opt/entrypoint.sh"]
