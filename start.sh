#!/bin/bash
python manage.py migrate
gunicorn isp_billing.wsgi:application
