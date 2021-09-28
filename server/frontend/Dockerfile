FROM node:14-buster-slim
LABEL maintainer="Pouria Hadjibagheri <Pouria.Hadjibagheri@phe.gov.uk>"

COPY ../../app/static_private/covid19-cms           /app/covid19-cms

WORKDIR /app/covid19-cms

RUN rm -rf node_modules && \
    npm install         && \
    npx browserslist@latest --update-db

EXPOSE 3000