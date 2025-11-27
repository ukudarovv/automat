@echo off
echo Starting Django server on port 8001...
cd /d %~dp0
python manage.py runserver 0.0.0.0:8001
pause

