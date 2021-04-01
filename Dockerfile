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


FROM python:3.9.2-buster
LABEL maintainer="Pouria Hadjibagheri <Pouria.Hadjibagheri@phe.gov.uk>"

# Gunicorn binding port
ENV GUNICORN_PORT 5000

#COPY server/install-nginx.sh          /install-nginx.sh
#
#RUN bash /install-nginx.sh
#RUN rm /etc/nginx/conf.d/default.conf

RUN apt-get update                                                   && \
    apt-get upgrade -y --no-install-recommends --no-install-suggests && \
    rm -rf /var/lib/apt/lists/*


RUN addgroup --system --gid 102 app                                  && \
    adduser  --system --disabled-login --ingroup app                    \
             --no-create-home --home /nonexistent                       \
             --gecos "app user" --shell /bin/false --uid 102 app

# Install Supervisord
RUN apt-get update                             && \
    apt-get upgrade -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

#COPY server/base.nginx               ./nginx.conf
#COPY server/upload.nginx              /etc/nginx/conf.d/upload.conf
#COPY server/engine.nginx              /etc/nginx/conf.d/engine.conf

COPY ./requirements.txt               /app/requirements.txt

RUN python3 -m pip install --no-cache-dir -U pip                      && \
    python3 -m pip install --no-cache-dir setuptools                  && \
    python3 -m pip install -U --no-cache-dir -r /app/requirements.txt && \
    rm /app/requirements.txt

# Gunicorn config / entrypoint
COPY server/gunicorn_conf.py        /gunicorn_conf.py
COPY server/start-gunicorn.sh       /start-gunicorn.sh
RUN chmod +x /start-gunicorn.sh
#COPY ./start-reload.sh /start-reload.sh
#RUN chmod +x /start-reload.sh

# Custom Supervisord config
#COPY server/supervisord.conf          /etc/supervisor/conf.d/supervisord.conf

# Main service entrypoint - launches supervisord
#COPY server/entrypoint.sh             /entrypoint.sh
#RUN chmod +x /entrypoint.sh


WORKDIR /app

COPY ./server/uvicorn_worker.py                /app/app/uvicorn_worker.py
COPY ./app/                                    /app/app/
COPY --from=builder /app/static_private/css    /app/app/static_private/css/
#RUN chown -R app /app

ENV PYTHONPATH /app/app

USER app

EXPOSE 5000

ENTRYPOINT ["/start-gunicorn.sh"]
