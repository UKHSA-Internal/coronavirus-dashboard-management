#!/usr/bin bash

npx postcss ./css/dist/application.css --use autoprefixer -d ./css
uglifycss ./css/dist/application.css --output ./css/dist/application.css
