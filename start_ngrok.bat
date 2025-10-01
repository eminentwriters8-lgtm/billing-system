@echo off
cd /d "F:\Billing System"
echo Waiting for server to start...
timeout /t 3
echo Starting ngrok tunnel...
ngrok.exe http 8080 --host-header="localhost:8080"
pause