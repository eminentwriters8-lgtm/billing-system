web: python manage.py migrate && gunicorn isp_billing.wsgi:application
release: python manage.py migrate