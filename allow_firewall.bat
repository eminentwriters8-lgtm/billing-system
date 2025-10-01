@echo off
netsh advfirewall firewall add rule name="Africa Online Networks" dir=in action=allow protocol=TCP localport=8080
echo Firewall rule added for port 8080
pause