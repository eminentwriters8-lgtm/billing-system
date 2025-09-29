release: python manage.py migrate && python create_admin.py
web: gunicorn isp_billing.wsgi:application