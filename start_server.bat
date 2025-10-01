@echo off
cd /d "F:\Billing System"
call venv\Scripts\activate.bat
python manage.py runserver 0.0.0.0:8080