#!/bin/sh

source virtualenvwrapper.sh 
# ~/.virtualenvs/django1.11/bin/python
workon django1.11
python manage.py  runserver 0.0.0.0:80 &

