#!/bin/sh

python manage.py graph_models -a -o ws.dot
dot ws -Tpng -o ws.png
